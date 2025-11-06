from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import timedelta, datetime
import hashlib
import secrets
import base64
from jose import JWTError, jwt

from ..models import User

# Secret in prototype only. Replace with env var in production.
SECRET_KEY = "change-me-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24


router = APIRouter()

class UserCreate(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

def verify_password(plain, hashed):
    # Verify a PBKDF2-SHA256 hash saved in the format:
    # pbkdf2_sha256$<iterations>$<salt_hex>$<dk_hex>
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
    # Use PBKDF2-HMAC-SHA256 (built-in) to avoid bcrypt/passlib compatibility issues.
    # Format: pbkdf2_sha256$<iterations>$<salt_hex>$<dk_hex>
    password_norm = _normalize_password(password)
    salt = secrets.token_bytes(16)
    iterations = 100_000
    dk = hashlib.pbkdf2_hmac("sha256", password_norm.encode("utf-8"), salt, iterations)
    return f"pbkdf2_sha256${iterations}${salt.hex()}${dk.hex()}"


def _normalize_password(password: str) -> str:
    """Normalize a password to a utf-8 string truncated to 72 bytes.

    This ensures bcrypt won't raise ValueError for inputs >72 bytes while
    keeping verification consistent (we apply the same truncation on verify).
    """
    if password is None:
        return password
    if not isinstance(password, str):
        password = str(password)
    b = password.encode("utf-8", errors="ignore")
    if len(b) > 72:
        b = b[:72]
    return b.decode("utf-8", errors="ignore")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded

@router.post("/register", response_model=Token)
async def register(payload: UserCreate, request: Request):
    db = request.app.state.db
    existing = await db["users"].find_one({"email": payload.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    # If name is missing, derive a reasonable default from the email local-part
    name = payload.name or payload.email.split("@")[0]
    hashed = get_password_hash(payload.password)
    user_doc = {"name": name, "email": payload.email, "hashed_password": hashed, "created_at": datetime.utcnow()}
    result = await db["users"].insert_one(user_doc)
    token = create_access_token({"sub": str(result.inserted_id)})
    return {"access_token": token}


@router.post("/login", response_model=Token)
async def login(payload: UserCreate, request: Request):
    db = request.app.state.db
    user = await db["users"].find_one({"email": payload.email})
    if not user or not verify_password(payload.password, user.get("hashed_password")):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.get("_id"))})
    return {"access_token": token}
