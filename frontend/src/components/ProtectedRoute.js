import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function ProtectedRoute({ children }) {
  const { authenticated, loading } = useAuth();

  // Show a verification loading state while checking the user session
  if (loading) {
    return (
      <div className="app-bg" style={{ display: "flex", justifyContent: "center", alignItems: "center", minHeight: "100vh" }}>
        <div style={{ background: "rgba(255,255,255,0.9)", padding: "40px", borderRadius: "16px", boxShadow: "0 10px 30px rgba(0,0,0,0.15)", textAlign: "center" }}>
          <h2 style={{ margin: "0 0 10px", color: "#764ba2" }}>Telusko Trac</h2>
          <div className="loader">Verifying session...</div>
        </div>
      </div>
    );
  }

  // Redirect to login if user is not authenticated
  if (!authenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
}
