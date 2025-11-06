// frontend/src/components/TaskList.jsx

import React, { useState, useEffect } from "react";
import * as api from "../services/api";

// Helper function to assign CSS class based on priority score (0.0 to 1.0)
const getPriorityClass = (score) => {
  if (score >= 0.8) return "priority-high";
  if (score >= 0.5) return "priority-medium";
  return "priority-low";
};

export default function TaskList({ userId }) {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchTasks() {
      setError(null);
      setLoading(true);
      try {
        const data = await api.listTasks(userId);
        // Sort tasks descending by priority score for the display
        const sortedTasks = data.sort(
          (a, b) => b.priority_score - a.priority_score
        );
        setTasks(sortedTasks);
      } catch (err) {
        setError(err.message || "Failed to fetch tasks.");
      } finally {
        setLoading(false);
      }
    }

    fetchTasks();
  }, [userId]);

  if (loading) {
    return (
      <div style={{ textAlign: "center", padding: "20px" }}>
        Loading tasks...
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

  if (tasks.length === 0) {
    return (
      <div style={{ textAlign: "center", padding: "20px" }}>
        No tasks yet. Add one above!
      </div>
    );
  }

  return (
    <ul id="taskList">
      {tasks.map((task) => (
        <li key={task.id} className={getPriorityClass(task.priority_score)}>
          <div className="task-info">
            <div className="task-title">{task.title}</div>
            <div className="task-meta">
              Importance: {task.importance} | Energy: {task.energy} | Est:{" "}
              {task.time_estimate}m
            </div>
            {task.description && <small>{task.description}</small>}
          </div>
          <span className="priority-score">
            {task.priority_score.toFixed(2)}
          </span>
        </li>
      ))}
    </ul>
  );
}
