// frontend/src/App.jsx (FINAL CORRECTED CODE)

import React, { useState, useEffect } from "react";
import AuthForm from "./components/AuthForm";
import Dashboard from "./components/Dashboard"; // Dashboard component is ready to be used

export default function App() {
  // Initialize token state by checking localStorage
  const [token, setToken] = useState(() => {
    try {
      return localStorage.getItem("access_token");
    } catch (e) {
      return null;
    }
  });

  // Effect to manage the token persistence in localStorage
  useEffect(() => {
    if (token) localStorage.setItem("access_token", token);
    else localStorage.removeItem("access_token");
  }, [token]);

  // Function to clear the token and log out the user
  const handleLogout = () => setToken(null);

  return (
    <div>
      {!token ? (
        // 1. If NOT logged in, show the AuthForm
        <div className="auth-container">
          <AuthForm onSuccess={(t) => setToken(t)} />
        </div>
      ) : (
        // 2. If logged in, show the Dashboard component
        // This is the CRUCIAL change: replacing the static welcome div
        <Dashboard onLogout={handleLogout} />
      )}
    </div>
  );
}
