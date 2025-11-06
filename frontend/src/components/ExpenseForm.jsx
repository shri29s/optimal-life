// frontend/src/components/ExpenseForm.jsx

import React, { useState } from "react";
import * as api from "../services/api";

const initialForm = {
  description: "",
  amount: 0.0,
};

export default function ExpenseForm({ userId, onExpenseAdded }) {
  const [form, setForm] = useState(initialForm);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setForm({
      ...form,
      [name]: type === "number" ? Number(value) : value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const newExpense = { ...form, user_id: userId };
      await api.addExpense(newExpense);

      setForm(initialForm); // Reset form on success
      onExpenseAdded(); // Notify dashboard to refresh list
    } catch (err) {
      setError(err.message || "Failed to add expense.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-container">
      <h2>💸 Log New Expense</h2>
      <form
        className="expense-form"
        onSubmit={handleSubmit}
        id="addExpenseForm"
      >
        {error && <div className="auth-error">{error}</div>}

        <input
          type="text"
          name="description"
          value={form.description}
          onChange={handleChange}
          placeholder="Description (e.g., Coffee, Amazon order)"
          required
        />

        <div className="input-group">
          <label>Amount (USD):</label>
          <input
            type="number"
            name="amount"
            value={form.amount}
            onChange={handleChange}
            min="0.01"
            step="0.01"
            required
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? "Logging..." : "Log Expense"}
        </button>
      </form>
    </div>
  );
}
