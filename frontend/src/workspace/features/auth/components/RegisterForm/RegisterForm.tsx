import { useState } from "react";
import type { FormEvent } from "react";

import {
  register,
  type RegisterResponse,
} from "../../../../services/auth/auth.service";

import styles from "./RegisterForm.module.css";

interface RegisterFormProps {
  onRegistered: (email: string) => void;
  onBackToLogin: () => void;
  onClose: () => void;
}

export default function RegisterForm({
  onRegistered,
  onBackToLogin,
  onClose,
}: RegisterFormProps) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setError("");

    const trimmedName = name.trim();
    const trimmedEmail = email.trim();

    // -----------------------------
    // Validation
    // -----------------------------

    if (trimmedName.length < 2) {
      setError("Please enter your full name.");
      return;
    }

    if (!trimmedEmail) {
      setError("Please enter your email address.");
      return;
    }

    if (password.length < 8) {
      setError(
        "Password must contain at least 8 characters.",
      );
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    // -----------------------------
    // Register
    // -----------------------------

    try {
      setIsSubmitting(true);

      const response: RegisterResponse = await register({
        name: trimmedName,
        email: trimmedEmail,
        password,
      });

      if (!response.email) {
        throw new Error(
          "Registration completed but no email was returned.",
        );
      }

      /*
       * Registration succeeded.
       *
       * We do NOT log the user in here.
       *
       * The parent component should now display
       * the email verification form.
       */
      onRegistered(response.email);
    } catch (error: unknown) {
      console.error("Registration failed:", error);

      const axiosError = error as {
        response?: {
          data?: {
            detail?: unknown;
          };
        };
      };

      const detail = axiosError.response?.data?.detail;

      if (typeof detail === "string") {
        setError(detail);
      } else if (Array.isArray(detail)) {
        const messages = detail
          .map((item) => {
            if (
              typeof item === "object" &&
              item !== null &&
              "msg" in item
            ) {
              return String(
                (item as { msg?: unknown }).msg ?? "",
              );
            }

            return "";
          })
          .filter(Boolean);

        setError(
          messages.length > 0
            ? messages.join(" ")
            : "Unable to create your account. Please try again.",
        );
      } else if (error instanceof Error) {
        setError(error.message);
      } else {
        setError(
          "Unable to create your account. Please try again.",
        );
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className={styles.content}>
      {/* Header */}
      <div className={styles.header}>
        <div>
          <h2>Create your account</h2>

          <p>
            Create an account to continue optimizing
            your resume.
          </p>
        </div>

        <button
          type="button"
          className={styles.closeButton}
          onClick={onClose}
          aria-label="Close"
          disabled={isSubmitting}
        >
          ×
        </button>
      </div>

      {/* Registration form */}
      <form
        className={styles.form}
        onSubmit={handleSubmit}
      >
        {/* Full name */}
        <label className={styles.field}>
          <span>Full name</span>

          <input
            type="text"
            value={name}
            onChange={(event) =>
              setName(event.target.value)
            }
            placeholder="Raviteja Hegde"
            autoComplete="name"
            disabled={isSubmitting}
          />
        </label>

        {/* Email */}
        <label className={styles.field}>
          <span>Email</span>

          <input
            type="email"
            value={email}
            onChange={(event) =>
              setEmail(event.target.value)
            }
            placeholder="you@example.com"
            autoComplete="email"
            disabled={isSubmitting}
          />
        </label>

        {/* Password */}
        <label className={styles.field}>
          <span>Password</span>

          <input
            type="password"
            value={password}
            onChange={(event) =>
              setPassword(event.target.value)
            }
            placeholder="At least 8 characters"
            autoComplete="new-password"
            disabled={isSubmitting}
          />
        </label>

        {/* Confirm password */}
        <label className={styles.field}>
          <span>Confirm password</span>

          <input
            type="password"
            value={confirmPassword}
            onChange={(event) =>
              setConfirmPassword(event.target.value)
            }
            placeholder="Enter your password again"
            autoComplete="new-password"
            disabled={isSubmitting}
          />
        </label>

        {/* Error */}
        {error && (
          <div
            className={styles.error}
            role="alert"
          >
            {error}
          </div>
        )}

        {/* Submit */}
        <button
          type="submit"
          className={styles.submitButton}
          disabled={isSubmitting}
        >
          {isSubmitting
            ? "Creating account..."
            : "Create account"}
        </button>
      </form>

      {/* Footer */}
      <div className={styles.footer}>
        <span>
          Already have an account?
        </span>

        <button
          type="button"
          className={styles.linkButton}
          onClick={onBackToLogin}
          disabled={isSubmitting}
        >
          Sign in
        </button>
      </div>
    </div>
  );
}