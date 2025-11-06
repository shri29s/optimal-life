// frontend/src/components/HabitList.jsx

import React, { useState, useEffect } from "react";
import * as api from "../services/api";

export default function HabitList({ userId }) {
  const [habits, setHabits] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchHabits() {
      setError(null);
      setLoading(true);
      try {
        const data = await api.listHabits(userId);
        // Display habits newest first
        const sortedHabits = data.sort(
          (a, b) =>
            new Date(b.id.getTimestamp()) - new Date(a.id.getTimestamp())
        );
        setHabits(sortedHabits.slice(0, 5)); // Show only the 5 most recent
      } catch (err) {
        setError(err.message || "Failed to fetch habits.");
      } finally {
        setLoading(false);
      }
    }

    fetchHabits();
  }, [userId]);

  if (loading) {
    return (
      <div style={{ textAlign: "center", padding: "20px" }}>
        Loading habits...
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

  if (habits.length === 0) {
    return (
      <div style={{ textAlign: "center", padding: "20px" }}>
        No habits logged yet.
      </div>
    );
  }

  return (
    <div>
      <h3>Recent Habit Logs (Top 5)</h3>
      <ul id="habitList" style={{ listStyle: "none", padding: 0 }}>
        {habits.map((h, index) => (
          <li
            key={h.id}
            style={{
              background: index % 2 === 0 ? "#f0f4f8" : "#e2e8f0",
              padding: "12px 15px",
              borderRadius: "6px",
              marginBottom: "8px",
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: "10px",
            }}
          >
            <div style={{ fontWeight: "bold" }}>
              {new Date(h.id.getTimestamp()).toLocaleDateString()}
            </div>
            <div>
              Sleep: {h.sleep_hours}h | Exercise: {h.exercise_minutes}m
            </div>
            <div
              style={{
                color:
                  h.mood > 7 ? "#10b981" : h.mood < 4 ? "#ef4444" : "#f59e0b",
              }}
            >
              Mood: {h.mood}/10
            </div>
            <div style={{ fontSize: "0.9em", color: "#4b5563" }}>
              Caffeine: {h.caffeine_mg}mg
            </div>
            {/* The correlation field is not set by the router, 
                but we show the data logged anyway */}
          </li>
        ))}
      </ul>
    </div>
  );
}
