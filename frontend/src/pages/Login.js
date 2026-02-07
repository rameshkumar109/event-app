import React, { useState } from "react";
import "./Login.css";

export default function Login({ errorOverride = "" }) {
  const API_BASE =
    process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:5000";
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(errorOverride);

  const validateEmail = (value) => {
    return /\S+@\S+\.\S+/.test(value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!validateEmail(email)) {
      setError("Please enter a valid email address.");
      return;
    }
    if (!password || password.length < 6) {
      setError("Password must be at least 6 characters.");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();
      if (!res.ok) {
        const msg = data.error || data.message || "Invalid credentials";
        throw new Error(msg);
      }

      if (data.token) {
        localStorage.setItem("gt_user_token", data.token);
        // go to home or refresh app state
        window.location.href = "/";
      } else {
        throw new Error("No token returned from server");
      }
    } catch (err) {
      setError(err.message || "Failed to sign in. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="gt-login-root">
      {/* fixed header brand so site name is always visible */}
      <header className="gt-topbar">
        <div className="brand-pill">
          <span className="brand-dot" /> GloboTicket
        </div>
      </header>

  <div className="gt-login-left">
        <h1>Welcome back to the world of live moments.</h1>
        <p>Sign in to track artists, save seats, and get early access drops.</p>
        <div className="hero-metrics">
          <div>
            <strong>4.8M</strong>
            <span>tickets scanned</span>
          </div>
          <div>
            <strong>120+</strong>
            <span>venues onboarded</span>
          </div>
          <div>
            <strong>24/7</strong>
            <span>fan support</span>
          </div>
        </div>
      </div>

      <div className="gt-login-card">
        <div className="card-header">
          <h2>Sign in</h2>
          <p>Use your GloboTicket account to continue.</p>
        </div>

        <form className="login-form" onSubmit={handleSubmit}>
          {error && <div className="gt-error">{error}</div>}

          <label className="field">
            <span>Email address</span>
            <input
              type="email"
              placeholder="you@domain.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </label>

          <label className="field">
            <span>Password</span>
            <input
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </label>

          <div className="form-row">
            <label className="checkbox">
              <input type="checkbox" /> Remember me for 30 days
            </label>
            <button type="button" className="link-button">
              Forgot password?
            </button>
          </div>

          <button className="primary-button" type="submit" disabled={loading}>
            {loading ? "Signing in..." : "Sign in"}
          </button>

          <div className="divider">
            <span>or</span>
          </div>

          <div className="socials">
            <button
              className="ghost-button"
              type="button"
              onClick={() => (window.location.href = `${API_BASE}/auth/google`)}
            >
              Continue with Google
            </button>
            <button className="ghost-button" type="button">
              Continue with Apple
            </button>
          </div>
        </form>

        <p className="signup-text">
          New here? <button className="link-button" type="button" onClick={() => (window.location.href = "/register")}>
            Create an account
          </button>
        </p>
      </div>
    </div>
  );
}
