from fastapi import APIRouter, HTTPException, Depends, Request, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import timedelta, datetime
import hashlib
import secrets
import base64
from jose import JWTError, jwt
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from ..database import get_db_dependency # Dependency to access the database
from ..models import User

# Secret in prototype only. Replace with env var in production.
SECRET_KEY = "change-me-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24

# Security scheme for FastAPI to look for a token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token") 

router = APIRouter()

class UserCreate(BaseModel):
    # Name is now required, removing Optional[str] = None
    name: str 
    email: EmailStr
    password: str
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    sub: Optional[str] = None # 'sub' will hold the user ID (ObjectId string)

# --- Password Utilities (unchanged, but moved to the top) ---

def _normalize_password(password: str) -> str:
    """Normalize a password to a utf-8 string truncated to 72 bytes."""
    if password is None:
        return password
    if not isinstance(password, str):
        password = str(password)
    b = password.encode("utf-8", errors="ignore")
    if len(b) > 72:
        b = b[:72]
    return b.decode("utf-8", errors="ignore")

def verify_password(plain: str, hashed: str) -> bool:
    # Verifies the PBKDF2-SHA256 hash saved in the format: pbkdf2_sha256$<iterations>$<salt_hex>$<dk_hex>
    if plain is None or hashed is None:
        return False
    plain_norm = _normalize_password(plain)
    try:
        parts = hashed.split("$")
        if len(parts) != 4 or not parts[0].startswith("pbkdf2_sha256"):
            return False
        _, iterations_s, salt_hex, dk_hex = parts
        iterations = int(iterations_s)
        salt = bytes.fromhex(salt_hex)
        dk = bytes.fromhex(dk_hex)
        new_dk = hashlib.pbkdf2_hmac("sha256", plain_norm.encode("utf-8"), salt, iterations)
        return secrets.compare_digest(new_dk, dk)
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    # Generates PBKDF2-HMAC-SHA256 hash
    password_norm = _normalize_password(password)
    salt = secrets.token_bytes(16)
    iterations = 100_000
    dk = hashlib.pbkdf2_hmac("sha256", password_norm.encode("utf-8"), salt, iterations)
    return f"pbkdf2_sha256${iterations}${salt.hex()}${dk.hex()}"


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded

# --- Dependency Function ---

async def get_current_user(
    db: AsyncIOMotorDatabase = Depends(get_db_dependency),
    token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        token_data = TokenData(sub=user_id_str)
    except JWTError:
        raise credentials_exception

    # Fetch user from MongoDB
    user_doc = await db["users"].find_one({"_id": ObjectId(token_data.sub)})
    
    if user_doc is None:
        raise credentials_exception
    
    # Return user data parsed into the Pydantic model
    return User.parse_obj(user_doc)


# --- Router Endpoints ---

@router.post("/register", response_model=Token)
async def register(payload: UserCreate, db: AsyncIOMotorDatabase = Depends(get_db_dependency)):
    users_collection = db["users"]
    
    existing = await users_collection.find_one({"email": payload.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed = get_password_hash(payload.password)
    
    # Pydantic validation handles 'name' and 'email' being required
    user_doc = {
        "name": payload.name, 
        "email": payload.email, 
        "hashed_password": hashed, 
        "created_at": datetime.utcnow()
    }
    
    result = await users_collection.insert_one(user_doc)
    
    # Get the MongoDB ObjectId string
    user_id_str = str(result.inserted_id)
    
    token = create_access_token({"sub": user_id_str})
    return {"access_token": token}


@router.post("/login", response_model=Token)
async def login(payload: UserLogin, db: AsyncIOMotorDatabase = Depends(get_db_dependency)):
    users_collection = db["users"]
    
    # Find user by email
    user_doc = await users_collection.find_one({"email": payload.email})

    if not user_doc or not verify_password(payload.password, user_doc.get("hashed_password")):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # The MongoDB _id must be converted to string for the token payload
    token = create_access_token({"sub": str(user_doc.get("_id"))})
    return {"access_token": token}