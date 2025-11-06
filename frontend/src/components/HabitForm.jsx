// frontend/src/components/HabitForm.jsx

import React, { useState } from "react";
import * as api from "../services/api";

const initialForm = {
  sleep_hours: 7.0,
  exercise_minutes: 30,
  caffeine_mg: 50,
  mood: 5, // 1 (Bad) to 10 (Great)
};

export default function HabitForm({ userId, onHabitAdded }) {
  const [form, setForm] = useState(initialForm);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value, type } = e.target;

    // Convert to number if the field type is number and value is not empty, otherwise keep it or default to 0 for required fields.
    let parsedValue = value;
    if (type === "number") {
      // Use parseFloat for sleep_hours, parseInt for exercise/caffeine/mood
      if (name === "sleep_hours") {
        parsedValue = value === "" ? null : parseFloat(value);
      } else {
        parsedValue = value === "" ? null : parseInt(value);
      }
    }

    setForm({
      ...form,
      [name]: parsedValue, // Use the parsed or default value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const newHabit = { ...form, user_id: userId };
      // 1. Log the habit
      await api.addHabit(newHabit);

      setForm(initialForm); // Reset form on success
      onHabitAdded(); // Notify dashboard to refresh list
    } catch (err) {
      setError(err.message || "Failed to log habit.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-container">
      <h2>🧠 Log Daily Habits</h2>
      <form className="habit-form" onSubmit={handleSubmit} id="addHabitForm">
        {error && <div className="auth-error">{error}</div>}

        <div className="input-group">
          <label>Sleep (hours):</label>
          <input
            type="number"
            name="sleep_hours"
            value={form.sleep_hours}
            onChange={handleChange}
            min="0"
            max="12"
            step="0.1"
            required
          />
        </div>

        <div className="input-group">
          <label>Exercise (minutes):</label>
          <input
            type="number"
            name="exercise_minutes"
            value={form.exercise_minutes}
            onChange={handleChange}
            min="0"
            required
          />
        </div>

        <div className="input-group">
          <label>Caffeine (mg):</label>
          <input
            type="number"
            name="caffeine_mg"
            value={form.caffeine_mg}
            onChange={handleChange}
            min="0"
            required
          />
        </div>

        <div className="input-group">
          <label>Mood (1-10):</label>
          <input
            type="number"
            name="mood"
            value={form.mood}
            onChange={handleChange}
            min="1"
            max="10"
            required
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? "Logging..." : "Log Day"}
        </button>
      </form>
    </div>
  );
}
