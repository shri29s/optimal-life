// frontend/src/components/TaskForm.jsx

import React, { useState } from "react";
import * as api from "../services/api";

const initialForm = {
  title: "",
  description: "",
  importance: 5, // 0-10
  energy: 5, // 0-10 (How much energy it requires)
  time_estimate: 30, // minutes
};

export default function TaskForm({ userId, onTaskAdded }) {
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
      // The backend (tasks.py) automatically calculates priority_score
      const newTask = { ...form, user_id: userId };
      await api.addTask(newTask);

      setForm(initialForm); // Reset form on success
      onTaskAdded(); // Notify dashboard to refresh list
    } catch (err) {
      setError(err.message || "Failed to add task.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="task-form" onSubmit={handleSubmit} id="addTaskForm">
      {error && <div className="auth-error">{error}</div>}

      <input
        type="text"
        name="title"
        value={form.title}
        onChange={handleChange}
        placeholder="Task Title (e.g., Finish report draft)"
        required
      />
      <textarea
        name="description"
        value={form.description}
        onChange={handleChange}
        placeholder="Optional description..."
      />

      <div className="input-group">
        <label>Importance (0-10):</label>
        <input
          type="number"
          name="importance"
          value={form.importance}
          onChange={handleChange}
          min="0"
          max="10"
          required
        />
      </div>
      <div className="input-group">
        <label>Energy Required (0-10):</label>
        <input
          type="number"
          name="energy"
          value={form.energy}
          onChange={handleChange}
          min="0"
          max="10"
          required
        />
      </div>
      <div className="input-group">
        <label>Time Estimate (minutes):</label>
        <input
          type="number"
          name="time_estimate"
          value={form.time_estimate}
          onChange={handleChange}
          min="5"
          required
        />
      </div>

      <button type="submit" disabled={loading}>
        {loading ? "Adding Task..." : "Add Task & Prioritize"}
      </button>
    </form>
  );
}
