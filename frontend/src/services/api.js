// frontend/src/services/api.js

const handleResponse = async (res) => {
  const text = await res.text();
  let data = null;
  try {
    data = text ? JSON.parse(text) : null;
  } catch (e) {
    data = text;
  }
  if (!res.ok) {
    // Extract the human-readable message from the backend response
    const msg = data?.detail || data?.message || text || `HTTP ${res.status}`;
    const err = new Error(msg);
    err.status = res.status;
    throw err;
  }
  return data;
};

// --- Authorization Helper ---

function getAuthHeaders() {
  const token = localStorage.getItem("access_token");
  if (!token) throw new Error("Authentication required.");

  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`, // Include the JWT for authorization
  };
}

// ------------------------------------------------------------------
// 🔐 Authentication Routes (Unprotected)
// ------------------------------------------------------------------

export async function register({ name, email, password }) {
  const res = await fetch("/api/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, password }),
  });
  return handleResponse(res);
}

// NOTE: This assumes you updated the backend /login route to use the new UserLogin model
export async function login({ email, password }) {
  const res = await fetch("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  return handleResponse(res);
}

// ------------------------------------------------------------------
// 📝 Protected Task Routes
// ------------------------------------------------------------------

/**
 * Adds a new task to the backend, which automatically calculates the priority score.
 * @param {object} taskData - Contains title, importance, energy, time_estimate, user_id
 */
export async function addTask(taskData) {
  const res = await fetch("/api/tasks/add", {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(taskData),
  });
  return handleResponse(res);
}

/**
 * Fetches the list of tasks for a given user.
 * @param {string} userId - The MongoDB ObjectId string of the user.
 */
export async function listTasks(userId) {
  const res = await fetch(`/api/tasks/list?user_id=${userId}`, {
    method: "GET",
    headers: getAuthHeaders(),
  });
  return handleResponse(res);
}

// ------------------------------------------------------------------
// 💵 Protected Expense Routes
// ------------------------------------------------------------------

/**
 * Adds a new expense to the backend.
 * @param {object} expenseData - Contains description, amount, user_id
 */
export async function addExpense(expenseData) {
  const res = await fetch("/api/expenses/add", {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(expenseData),
  });
  return handleResponse(res);
}

/**
 * Fetches the list of expenses for a given user.
 * @param {string} userId - The MongoDB ObjectId string of the user.
 */
export async function listExpenses(userId) {
  const res = await fetch(`/api/expenses/list?user_id=${userId}`, {
    method: "GET",
    headers: getAuthHeaders(),
  });
  return handleResponse(res);
}

// ------------------------------------------------------------------
// 😴 Protected Habit Routes
// ------------------------------------------------------------------

/**
 * Adds a new habit log to the backend.
 * @param {object} habitData - Contains sleep_hours, exercise_minutes, caffeine_mg, mood, user_id
 */
export async function addHabit(habitData) {
  const res = await fetch("/api/habits/add", {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(habitData),
  });
  return handleResponse(res);
}

/**
 * Fetches the list of habit logs for a given user.
 * @param {string} userId - The MongoDB ObjectId string of the user.
 */
export async function listHabits(userId) {
  const res = await fetch(`/api/habits/list?user_id=${userId}`, {
    method: "GET",
    headers: getAuthHeaders(),
  });
  return handleResponse(res);
}

// ------------------------------------------------------------------
// 📈 Protected Analytics Route
// ------------------------------------------------------------------

/**
 * Fetches the example ML insights from the backend.
 */
export async function getInsights() {
  const res = await fetch("/api/analytics/insights", {
    method: "GET",
    headers: getAuthHeaders(),
  });
  return handleResponse(res);
}
