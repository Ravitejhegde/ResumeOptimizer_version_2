import {
  useEffect,
  useRef,
  useState,
} from "react";

import type { FormEvent } from "react";

import { verifyEmail } from "../../../../services/auth/auth.service";

import styles from "./VerifyEmailForm.module.css";

interface VerifyEmailFormProps {
  email: string;
  onVerified: () => void;
  onBack: () => void;
  onClose: () => void;
}

export default function VerifyEmailForm({
  email,
  onVerified,
  onBack,
  onClose,
}: VerifyEmailFormProps) {
  const [otp, setOtp] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setError("");

    const normalizedOtp = otp
      .replace(/\D/g, "")
      .slice(0, 6);

    if (normalizedOtp.length !== 6) {
      setError(
        "Please enter the 6-digit verification code.",
      );
      return;
    }

    try {
      setIsSubmitting(true);

      const response = await verifyEmail({
        email,
        otp: normalizedOtp,
      });

      if (!response.verified) {
        setError(
          "Email verification was not completed.",
        );
        return;
      }

      onVerified();
    } catch (error: any) {
      console.error(
        "Email verification failed:",
        error,
      );

      const detail =
        error?.response?.data?.detail;

      if (typeof detail === "string") {
        setError(detail);
      } else if (Array.isArray(detail)) {
        const message = detail
          .map((item: any) => item?.msg)
          .filter(Boolean)
          .join(" ");

        setError(
          message ||
            "Invalid or expired verification code.",
        );
      } else {
        setError(
          "Invalid or expired verification code.",
        );
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  function handleOtpChange(value: string) {
    const digits = value
      .replace(/\D/g, "")
      .slice(0, 6);

    setOtp(digits);

    if (error) {
      setError("");
    }
  }

  return (
    <div className={styles.content}>
      <div className={styles.header}>
        <div>
          <h2>Verify your email</h2>

          <p>
            We sent a 6-digit verification code to:
          </p>

          <strong>{email}</strong>
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

      <form
        className={styles.form}
        onSubmit={handleSubmit}
      >
        <label className={styles.otpLabel}>
          <span>Verification code</span>

          <input
            ref={inputRef}
            className={styles.otpInput}
            type="text"
            inputMode="numeric"
            autoComplete="one-time-code"
            value={otp}
            onChange={(event) =>
              handleOtpChange(
                event.target.value,
              )
            }
            placeholder="000000"
            maxLength={6}
            disabled={isSubmitting}
            aria-label="6-digit verification code"
          />
        </label>

        <div className={styles.hint}>
          Check your inbox and spam folder for
          the verification email.
        </div>

        {error && (
          <div
            className={styles.error}
            role="alert"
          >
            {error}
          </div>
        )}

        <button
          type="submit"
          className={styles.submitButton}
          disabled={
            isSubmitting ||
            otp.length !== 6
          }
        >
          {isSubmitting
            ? "Verifying..."
            : "Verify email"}
        </button>
      </form>

      <div className={styles.footer}>
        <button
          type="button"
          className={styles.backButton}
          onClick={onBack}
          disabled={isSubmitting}
        >
          ← Change email
        </button>
      </div>
    </div>
  );
}