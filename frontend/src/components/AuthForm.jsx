import React, { useState } from "react";
import * as api from "../services/api";

export default function AuthForm({ onSuccess }) {
  const [mode, setMode] = useState("login"); // 'login' or 'register'
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      let data;
      if (mode === "register") {
        data = await api.register({ name, email, password });
      } else {
        data = await api.login({ email, password });
      }
      // Token is returned as access_token
      if (data?.access_token) {
        onSuccess(data.access_token);
      } else {
        setError("No access token received");
      }
    } catch (err) {
      setError(err.message || JSON.stringify(err, null, 2) || "Request failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>{mode === "register" ? "Create account" : "Sign in"}</h2>
      {error && <div className="auth-error">{error}</div>}
      <form className="auth-form" onSubmit={submit}>
        {mode === "register" && (
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Name (optional)"
            required // <--- ADD THE 'required' ATTRIBUTE
          />
        )}
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? "Working…" : mode === "register" ? "Register" : "Login"}
        </button>
      </form>
      <div className="auth-toggle">
        {mode === "register" ? (
          <small>
            Already have an account?{" "}
            <button
              onClick={() => {
                setMode("login");
                setName(""); // <--- RESET NAME STATE
              }}
            >
              Sign in
            </button>
          </small>
        ) : (
          <small>
            No account?{" "}
            <button onClick={() => setMode("register")}>Create one</button>
          </small>
        )}
      </div>
    </div>
  );
}
