import { useEffect, useState } from "react";

import styles from "./Header.module.css";

import {
  getCurrentUser,
  isAuthenticated,
  login,
  logout,
  type CurrentUser,
} from "../../services/auth/auth.service";

import { useWorkspace } from "../../store/useWorkspace";

import RegisterForm from "../../features/auth/components/RegisterForm/RegisterForm";
import VerifyEmailForm from "../../features/auth/components/VerifyEmailForm/VerifyEmailForm";

type AuthView =
  | "login"
  | "register"
  | "verify-email";

const Header = () => {
  const { setState } = useWorkspace();

  const [user, setUser] =
    useState<CurrentUser | null>(null);

  const [showLogin, setShowLogin] =
    useState(false);

  const [authView, setAuthView] =
    useState<AuthView>("login");

  const [verificationEmail, setVerificationEmail] =
    useState("");

  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  /* =========================================================
     Load Current User
  ========================================================= */

  useEffect(() => {
    const loadUser = async () => {
      if (!isAuthenticated()) {
        return;
      }

      try {
        const currentUser =
          await getCurrentUser();

        setUser(currentUser);

        setState((previous) => ({
          ...previous,
          user: currentUser,
          isAuthenticated: true,
        }));
      } catch {
        logout();

        setUser(null);

        setState((previous) => ({
          ...previous,
          user: null,
          isAuthenticated: false,
        }));
      }
    };

    void loadUser();
  }, [setState]);

  /* =========================================================
     Login
  ========================================================= */

  const openLogin = () => {
    setError("");
    setAuthView("login");
    setShowLogin(true);
  };

  const closeLogin = () => {
    if (loading) {
      return;
    }

    setShowLogin(false);
    setAuthView("login");

    setError("");
    setEmail("");
    setPassword("");
    setVerificationEmail("");
  };

  /* =========================================================
     Registration
  ========================================================= */

  const openRegister = () => {
    setError("");
    setAuthView("register");
  };

  const handleRegistered = (
    registeredEmail: string,
  ) => {
    setVerificationEmail(
      registeredEmail,
    );

    setEmail(
      registeredEmail,
    );

    setError("");
    setAuthView("verify-email");
  };

  /* =========================================================
     Email Verification
  ========================================================= */

  const handleVerified = () => {
    setEmail(
      verificationEmail,
    );

    setPassword("");

    setError("");

    setAuthView("login");
  };

  const handleBackToLogin = () => {
    setError("");
    setAuthView("login");
  };

  const handleBackToRegister = () => {
    setError("");
    setAuthView("register");
  };

  /* =========================================================
     Login Submit
  ========================================================= */

  const handleLogin = async () => {
    const normalizedEmail =
      email.trim();

    if (
      !normalizedEmail ||
      !password
    ) {
      setError(
        "Enter your email and password.",
      );

      return;
    }

    try {
      setLoading(true);
      setError("");

      await login({
        email: normalizedEmail,
        password,
      });

      const currentUser =
        await getCurrentUser();

      setUser(currentUser);

      setState((previous) => ({
        ...previous,
        user: currentUser,
        isAuthenticated: true,
      }));

      closeLogin();
    } catch {
      setError(
        "Unable to sign in. Please check your email and password.",
      );
    } finally {
      setLoading(false);
    }
  };

  /* =========================================================
     Logout
  ========================================================= */

  const handleLogout = () => {
    logout();

    setUser(null);

    setState((previous) => ({
      ...previous,
      user: null,
      isAuthenticated: false,
    }));
  };

  /* =========================================================
     Pricing Navigation
  ========================================================= */

  const handlePricing = () => {
    setShowLogin(false);

    setState((previous) => ({
      ...previous,
      step: "pricing",
    }));
  };

  /* =========================================================
     Render
  ========================================================= */

  return (
    <>
      <header className={styles.header}>

        {/* =====================================================
            Brand
        ===================================================== */}

        <div className={styles.brand}>

          <div className={styles.logo}>
            R
          </div>

          <div>
            <h1>
              ResumeOptimizer
            </h1>

            <p>
              Same Resume. Smarter Words.
            </p>
          </div>

        </div>

        {/* =====================================================
            Navigation
        ===================================================== */}

        <nav
          className={styles.actions}
        >

          {/* Pricing */}

          <button
            type="button"
            className={
              styles.secondaryButton
            }
            onClick={handlePricing}
          >
            Pricing
          </button>

          {/* Theme */}

          <button
            type="button"
            className={
              styles.secondaryButton
            }
          >
            Theme
          </button>

          {/* =================================================
              Authenticated User
          ================================================= */}

          {user ? (

            <button
              type="button"
              className={
                styles.userButton
              }
              onClick={handleLogout}
            >

              <span
                className={
                  styles.userIcon
                }
              >
                {user.name
                  .charAt(0)
                  .toUpperCase()}
              </span>

              <span>
                {user.name}
              </span>

            </button>

          ) : (

            <button
              type="button"
              className={
                styles.loginButton
              }
              onClick={openLogin}
            >
              Login
            </button>

          )}

        </nav>

      </header>

      {/* =======================================================
          Login / Registration Modal
      ======================================================= */}

      {showLogin && (

        <div
          className={styles.overlay}
          onMouseDown={(event) => {

            if (
              event.target ===
              event.currentTarget
            ) {
              closeLogin();
            }

          }}
        >

          <div
            className={styles.modal}
            role="dialog"
            aria-modal="true"
            aria-labelledby="auth-title"
          >

            {/* =================================================
                Login
            ================================================= */}

            {authView === "login" && (

              <>

                <div
                  className={
                    styles.modalHeader
                  }
                >

                  <div>

                    <h2 id="auth-title">
                      Welcome back
                    </h2>

                    <p>
                      Sign in to continue
                      optimizing your
                      resume.
                    </p>

                  </div>

                  <button
                    type="button"
                    className={
                      styles.closeButton
                    }
                    onClick={
                      closeLogin
                    }
                    disabled={loading}
                    aria-label="Close login"
                  >
                    ×
                  </button>

                </div>

                <div
                  className={
                    styles.form
                  }
                >

                  {/* Email */}

                  <label>
                    Email
                  </label>

                  <input
                    type="email"
                    placeholder="you@example.com"
                    value={email}
                    autoComplete="email"
                    disabled={loading}
                    onChange={(
                      event,
                    ) =>
                      setEmail(
                        event.target
                          .value,
                      )
                    }
                  />

                  {/* Password */}

                  <label>
                    Password
                  </label>

                  <input
                    type="password"
                    placeholder="Your password"
                    value={password}
                    autoComplete="current-password"
                    disabled={loading}
                    onChange={(
                      event,
                    ) =>
                      setPassword(
                        event.target
                          .value,
                      )
                    }
                    onKeyDown={(
                      event,
                    ) => {

                      if (
                        event.key ===
                        "Enter"
                      ) {
                        void handleLogin();
                      }

                    }}
                  />

                  {/* Error */}

                  {error && (

                    <div
                      className={
                        styles.error
                      }
                      role="alert"
                    >
                      {error}
                    </div>

                  )}

                  {/* Submit */}

                  <button
                    type="button"
                    className={
                      styles.submitButton
                    }
                    onClick={() =>
                      void handleLogin()
                    }
                    disabled={loading}
                  >

                    {loading
                      ? "Signing in..."
                      : "Sign in"}

                  </button>

                  {/* Register */}

                  <div
                    style={{
                      marginTop:
                        "18px",
                      textAlign:
                        "center",
                    }}
                  >

                    <span>
                      Don't have an
                      account?{" "}
                    </span>

                    <button
                      type="button"
                      onClick={
                        openRegister
                      }
                      disabled={loading}
                      style={{
                        border:
                          "none",
                        background:
                          "transparent",
                        padding: 0,
                        cursor:
                          "pointer",
                        fontWeight:
                          600,
                        color:
                          "#2563eb",
                      }}
                    >
                      Create account
                    </button>

                  </div>

                </div>

              </>

            )}

            {/* =================================================
                Registration
            ================================================= */}

            {authView ===
              "register" && (

              <RegisterForm
                onRegistered={
                  handleRegistered
                }
                onBackToLogin={
                  handleBackToLogin
                }
                onClose={
                  closeLogin
                }
              />

            )}

            {/* =================================================
                Email Verification
            ================================================= */}

            {authView ===
              "verify-email" && (

              <VerifyEmailForm
                email={
                  verificationEmail
                }
                onVerified={
                  handleVerified
                }
                onBack={
                  handleBackToRegister
                }
                onClose={
                  closeLogin
                }
              />

            )}

          </div>

        </div>

      )}

    </>
  );
};

export default Header;