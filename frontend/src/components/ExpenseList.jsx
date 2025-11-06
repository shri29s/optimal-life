// frontend/src/components/ExpenseList.jsx

import React, { useState, useEffect } from "react";
import * as api from "../services/api";

export default function ExpenseList({ userId }) {
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Note: We'll use a local state to trigger refetching if expenses change
  const [fetchKey, setFetchKey] = useState(0);

  useEffect(() => {
    async function fetchExpenses() {
      setError(null);
      setLoading(true);
      try {
        const data = await api.listExpenses(userId);
        // Sort expenses by date, newest first
        const sortedExpenses = data.sort(
          (a, b) => new Date(b.date) - new Date(a.date)
        );
        setExpenses(sortedExpenses);
      } catch (err) {
        setError(err.message || "Failed to fetch expenses.");
      } finally {
        setLoading(false);
      }
    }

    fetchExpenses();
  }, [userId, fetchKey]);

  // We expose a function to trigger a manual refetch
  ExpenseList.refetch = () => setFetchKey((prev) => prev + 1);

  if (loading) {
    return (
      <div style={{ textAlign: "center", padding: "20px" }}>
        Loading expenses...
      </div>
    );
  }

  if (error) {
    return (
      <div className="auth-error" style={{ maxWidth: "none" }}>
        Error: {error}
      </div>
    );
  }

  if (expenses.length === 0) {
    return (
      <div style={{ textAlign: "center", padding: "20px" }}>
        No expenses logged yet.
      </div>
    );
  }

  return (
    <div>
      <h3>Recent Expenses</h3>
      <ul id="expenseList" style={{ listStyle: "none", padding: 0 }}>
        {expenses.map((exp) => (
          <li
            key={exp.id}
            style={{
              background: "#f1f5f9",
              padding: "10px 15px",
              borderRadius: "6px",
              marginBottom: "8px",
              display: "flex",
              justifyContent: "space-between",
            }}
          >
            <span>{exp.description}</span>
            <span
              style={{
                fontWeight: "bold",
                color: exp.amount > 50 ? "#e53e3e" : "#2d3748",
              }}
            >
              ${exp.amount.toFixed(2)}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
