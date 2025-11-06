// frontend/src/components/Dashboard.jsx (FINAL INTEGRATED VERSION)

import React, { useState } from "react";
import TaskForm from "./TaskForm";
import TaskList from "./TaskList";
import ExpenseForm from "./ExpenseForm";
import ExpenseList from "./ExpenseList";
import HabitForm from "./HabitForm"; // <-- NEW IMPORT
import HabitList from "./HabitList"; // <-- NEW IMPORT

// PROTOTYPE HACK: Static example user ID
const PROTOTYPE_USER_ID = "60c72b2f9f1b2c3a4e5d6f78";

export default function Dashboard({ onLogout }) {
  const [taskKey, setTaskKey] = useState(0);
  const [expenseKey, setExpenseKey] = useState(0);
  const [habitKey, setHabitKey] = useState(0); // <-- NEW STATE

  const handleTaskAdded = () => setTaskKey((prev) => prev + 1);
  const handleExpenseAdded = () => setExpenseKey((prev) => prev + 1);
  const handleHabitAdded = () => setHabitKey((prev) => prev + 1); // <-- NEW HANDLER

  return (
    <div className="container">
      <header
        className="dashboard-header"
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <h1>Optimal Life Dashboard</h1>
        <button
          onClick={onLogout}
          className="logout-button"
          style={{ width: "auto", padding: "8px 16px" }}
        >
          Logout
        </button>
      </header>

      <div
        className="dashboard-grid"
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "30px",
          marginTop: "20px",
        }}
      >
        {/* --- LEFT COLUMN: Tasks --- */}
        <div>
          <div className="task-section form-container">
            <h2>🎯 Add a New Task</h2>
            <TaskForm
              userId={PROTOTYPE_USER_ID}
              onTaskAdded={handleTaskAdded}
            />
          </div>

          <div className="task-section" style={{ marginTop: "30px" }}>
            <h2>📝 Prioritized Task List</h2>
            <TaskList key={taskKey} userId={PROTOTYPE_USER_ID} />
          </div>
        </div>

        {/* --- RIGHT COLUMN: Expenses & Habits --- */}
        <div>
          <div style={{ marginBottom: "30px" }}>
            <ExpenseForm
              userId={PROTOTYPE_USER_ID}
              onExpenseAdded={handleExpenseAdded}
            />

            <div className="expense-section" style={{ marginTop: "30px" }}>
              <ExpenseList key={expenseKey} userId={PROTOTYPE_USER_ID} />
            </div>
          </div>

          {/* --- HABITS SECTION --- */}
          <div style={{ borderTop: "1px solid #e2e8f0", paddingTop: "30px" }}>
            <HabitForm
              userId={PROTOTYPE_USER_ID}
              onHabitAdded={handleHabitAdded}
            />
            <div className="habit-section" style={{ marginTop: "30px" }}>
              <HabitList key={habitKey} userId={PROTOTYPE_USER_ID} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
