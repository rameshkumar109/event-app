import React, { useState } from "react";
import "./Register.css";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const validateEmail = (value) => /\S+@\S+\.\S+/.test(value);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (!validateEmail(email)) return setError("Enter a valid email");
    if (password.length < 6) return setError("Password must be at least 6 characters");
    if (password !== confirm) return setError("Passwords do not match");

    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:5000/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Registration failed");
      // store token and redirect to home
      if (data.token) localStorage.setItem("gt_user_token", data.token);
      setSuccess("Account created — redirecting...");
      setTimeout(() => (window.location.href = "/"), 900);
    } catch (err) {
      setError(err.message || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="gt-login-root">
      <header className="gt-topbar">
        <div className="brand-pill">
          <span className="brand-dot" /> event-app
        </div>
      </header>

      <div className="gt-login-card">
        <div className="card-header">
          <h2>Create account</h2>
          <p>Register a new event-app account.</p>
        </div>

        <form className="login-form" onSubmit={handleSubmit}>
          {error && <div className="gt-error">{error}</div>}
          {success && <div className="gt-success">{success}</div>}

          <label className="field">
            <span>Email address</span>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@domain.com" required />
          </label>

          <label className="field">
            <span>Password</span>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" required />
          </label>

          <label className="field">
            <span>Confirm Password</span>
            <input type="password" value={confirm} onChange={(e) => setConfirm(e.target.value)} placeholder="••••••••" required />
          </label>

          <button className="primary-button" type="submit" disabled={loading}>{loading ? "Creating..." : "Create account"}</button>

          <div className="divider"><span>or</span></div>

          <div className="signup-text">Already have an account? <button type="button" className="link-button" onClick={() => (window.location.href = "/")}>Sign in</button></div>
        </form>
      </div>
    </div>
  );
}
