import React, { createContext, useContext, useState, useEffect } from "react";
import api from "../api/apiClient";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(null);
  const [authenticated, setAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  // Check user session status on startup
  useEffect(() => {
    async function checkSession() {
      try {
        const res = await api.get("/api/v1/auth/me");
        if (res.data && res.data.success) {
          setCurrentUser(res.data.data.user);
          setAuthenticated(true);
        } else {
          setCurrentUser(null);
          setAuthenticated(false);
        }
      } catch (err) {
        console.log("No active user session found.");
        setCurrentUser(null);
        setAuthenticated(false);
      } finally {
        setLoading(false);
      }
    }
    checkSession();
  }, []);

  // Interceptor to catch 401 Unauthorized errors and force logout
  useEffect(() => {
    const interceptor = api.interceptors.response.use(
      (response) => response,
      (err) => {
        if (err.response?.status === 401) {
          setCurrentUser(null);
          setAuthenticated(false);
        }
        return Promise.reject(err);
      }
    );
    return () => {
      api.interceptors.response.eject(interceptor);
    };
  }, []);

  const login = async (email, password) => {
    try {
      const res = await api.post("/api/v1/auth/login", { email, password });
      if (res.data && res.data.success) {
        setCurrentUser(res.data.data.user);
        setAuthenticated(true);
        return { success: true, message: res.data.message };
      }
      return { success: false, message: res.data.message || "Failed to log in." };
    } catch (err) {
      const errorMsg = err.response?.data?.message || "Invalid credentials or login error.";
      return { success: false, message: errorMsg };
    }
  };

  const logout = async () => {
    try {
      await api.post("/api/v1/auth/logout");
    } catch (err) {
      console.error("Logout request failed:", err);
    } finally {
      setCurrentUser(null);
      setAuthenticated(false);
    }
  };

  const register = async (username, email, password) => {
    try {
      const res = await api.post("/api/v1/auth/register", {
        username,
        email,
        password,
      });
      if (res.data && res.data.success) {
        return { success: true, message: res.data.message };
      }
      return { success: false, message: res.data.message || "Registration failed." };
    } catch (err) {
      const detailMsg = err.response?.data?.detail;
      const parsedMsg = Array.isArray(detailMsg)
        ? detailMsg.map((d) => d.msg).join(", ")
        : detailMsg;
      const errorMsg = err.response?.data?.message || parsedMsg || "Registration failed.";
      return { success: false, message: errorMsg };
    }
  };

  return (
    <AuthContext.Provider
      value={{
        currentUser,
        authenticated,
        loading,
        login,
        logout,
        register,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
