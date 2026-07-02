import React, { useState, useEffect } from "react";
import { useNavigate, Link, Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "./Register.css";

export default function Register() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const [passChecks, setPassChecks] = useState({
    length: false,
    upper: false,
    lower: false,
    number: false,
    special: false,
  });

  const { register, login, authenticated } = useAuth();
  const navigate = useNavigate();

  // Run password complexity checks on change
  useEffect(() => {
    setPassChecks({
      length: password.length >= 8,
      upper: /[A-Z]/.test(password),
      lower: /[a-z]/.test(password),
      number: /\d/.test(password),
      special: /[!@#$%^&*(),.?":{}|<>]/.test(password),
    });
  }, [password]);

  if (authenticated) {
    return <Navigate to="/" replace />;
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      setLoading(false);
      return;
    }

    const allPassed = Object.values(passChecks).every(Boolean);
    if (!allPassed) {
      setError("Please satisfy all password complexity rules.");
      setLoading(false);
      return;
    }

    const registerRes = await register(username, email, password);
    if (registerRes.success) {
      setSuccess("Account created successfully! Logging you in...");
      // Auto login upon registration success
      const loginRes = await login(email, password);
      if (loginRes.success) {
        setTimeout(() => {
          navigate("/");
        }, 1500);
      } else {
        setSuccess("");
        setError("Registration successful! Please sign in manually.");
        setLoading(false);
      }
    } else {
      setError(registerRes.message);
      setLoading(false);
    }
  };

  return (
    <div className="auth-page app-bg">
      <div className="auth-card card">
        <div className="auth-header">
          <span className="auth-logo">📦</span>
          <h2>Create Account</h2>
          <p className="auth-subtitle">Join Telusko Trac Inventory</p>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              id="username"
              type="text"
              placeholder="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              minLength={3}
              maxLength={50}
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <input
              id="email"
              type="email"
              placeholder="name@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <div className="password-input-container">
              <input
                id="password"
                type={showPassword ? "text" : "password"}
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <button
                type="button"
                className="show-password-toggle"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? "Hide" : "Show"}
              </button>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password</label>
            <input
              id="confirmPassword"
              type="password"
              placeholder="••••••••"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>

          {/* Password complexity requirements list */}
          <div className="password-requirements">
            <p className="req-title">Password must contain:</p>
            <ul className="req-list">
              <li className={passChecks.length ? "met" : "unmet"}>
                <span className="bullet">{passChecks.length ? "✓" : "○"}</span> At least 8 characters
              </li>
              <li className={passChecks.upper ? "met" : "unmet"}>
                <span className="bullet">{passChecks.upper ? "✓" : "○"}</span> One uppercase letter (A-Z)
              </li>
              <li className={passChecks.lower ? "met" : "unmet"}>
                <span className="bullet">{passChecks.lower ? "✓" : "○"}</span> One lowercase letter (a-z)
              </li>
              <li className={passChecks.number ? "met" : "unmet"}>
                <span className="bullet">{passChecks.number ? "✓" : "○"}</span> One number (0-9)
              </li>
              <li className={passChecks.special ? "met" : "unmet"}>
                <span className="bullet">{passChecks.special ? "✓" : "○"}</span> One special symbol (e.g. @, #, $, !)
              </li>
            </ul>
          </div>

          {error && <div className="error-msg auth-error">{error}</div>}
          {success && <div className="success-msg auth-success">{success}</div>}

          <button className="btn auth-btn" type="submit" disabled={loading}>
            {loading ? "Registering..." : "Register"}
          </button>
        </form>

        <div className="auth-footer">
          <p>
            Already have an account? <Link to="/login">Sign In</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
