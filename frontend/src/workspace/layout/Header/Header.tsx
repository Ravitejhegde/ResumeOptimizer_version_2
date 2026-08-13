import { useEffect, useState } from "react";
import styles from "./Header.module.css";

import {
  getCurrentUser,
  isAuthenticated,
  login,
  logout,
  type CurrentUser,
} from "../../services/auth/auth.service";

const Header = () => {
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [showLogin, setShowLogin] = useState(false);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadUser = async () => {
      if (!isAuthenticated()) {
        return;
      }

      try {
        const currentUser = await getCurrentUser();
        setUser(currentUser);
      } catch {
        logout();
        setUser(null);
      }
    };

    void loadUser();
  }, []);

  const handleLogin = async () => {
    if (!email.trim() || !password) {
      setError("Enter your email and password.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      await login({
        email: email.trim(),
        password,
      });

      const currentUser = await getCurrentUser();

      setUser(currentUser);
      setShowLogin(false);

      setEmail("");
      setPassword("");
    } catch {
      setError("Login failed. Please check your credentials.");
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    setUser(null);
  };

  return (
    <>
      <header className={styles.header}>
        <div>
          <h1>ResumeOptimizer</h1>
          <p>Same Resume. Smarter Words.</p>
        </div>

        <nav className={styles.actions}>
          <button type="button">Pricing</button>

          <button type="button">Theme</button>

          {user ? (
            <div>
              <button
                type="button"
                onClick={handleLogout}
              >
                👤 {user.name}
              </button>
            </div>
          ) : (
            <button
              type="button"
              onClick={() => setShowLogin(true)}
            >
              Login
            </button>
          )}
        </nav>
      </header>

      {showLogin && (
        <div>
          <div>
            <h2>Login</h2>

            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(event) =>
                setEmail(event.target.value)
              }
            />

            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
            />

            {error && <p>{error}</p>}

            <button
              type="button"
              onClick={() => setShowLogin(false)}
            >
              Cancel
            </button>

            <button
              type="button"
              onClick={handleLogin}
              disabled={loading}
            >
              {loading ? "Logging in..." : "Login"}
            </button>
          </div>
        </div>
      )}
    </>
  );
};

export default Header;