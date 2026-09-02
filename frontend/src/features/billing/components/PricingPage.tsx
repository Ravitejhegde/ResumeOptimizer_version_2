import { useEffect, useState } from "react";

import {
  createCheckout,
  getPricing,
} from "../api/billingApi";

import type {
  BillingInterval,
  Pricing,
} from "../types/billing";

import { getCurrentUser } from "../../../workspace/services/auth/auth.service";

import styles from "../styles/PricingPage.module.css";

const PricingPage = () => {
  const [pricing, setPricing] = useState<Pricing[]>([]);

  const [interval, setInterval] =
    useState<BillingInterval>("monthly");

  const [loading, setLoading] =
    useState(true);

  const [checkoutPlan, setCheckoutPlan] =
    useState<string | null>(null);

  const [error, setError] =
    useState<string | null>(null);

  const [checkoutMessage, setCheckoutMessage] =
    useState<string | null>(null);

  /* =========================================================
     Load Pricing
  ========================================================= */

  useEffect(() => {
    const loadPricing = async () => {
      try {
        setLoading(true);
        setError(null);

        const result = await getPricing("IN");

        setPricing(
          result.filter(
            (item) => item.active,
          ),
        );
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Unable to load pricing.",
        );
      } finally {
        setLoading(false);
      }
    };

    void loadPricing();
  }, []);

  /* =========================================================
     Checkout
  ========================================================= */

  const handleCheckout = async (
    plan: Pricing,
  ) => {
    try {
      setCheckoutPlan(plan.plan_code);
      setError(null);
      setCheckoutMessage(null);

      const user =
        await getCurrentUser();

      const successUrl =
        `${window.location.origin}/billing/success`;

      const cancelUrl =
        `${window.location.origin}/billing/cancel`;

      const result =
        await createCheckout({
          email: user.email,
          name: user.name,
          country: plan.country_code,
          plan: plan.plan_code,
          interval,
          provider: plan.payment_provider,
          success_url: successUrl,
          cancel_url: cancelUrl,
        });

      if (!result.checkout_url) {
        throw new Error(
          "Checkout is currently unavailable.",
        );
      }

      window.location.href =
        result.checkout_url;

    } catch (err) {
      const message =
        err instanceof Error
          ? err.message
          : "Unable to start checkout.";

      /*
       * Stripe is currently not configured.
       *
       * Keep the UI user-friendly instead of exposing
       * provider/infrastructure errors.
       */
      if (
        message.toLowerCase().includes("stripe") ||
        message.toLowerCase().includes("price") ||
        message.toLowerCase().includes("checkout") ||
        message.toLowerCase().includes("provider")
      ) {
        setCheckoutMessage(
          "Online payments are currently being prepared. Please try again later.",
        );
      } else {
        setError(message);
      }

      setCheckoutPlan(null);
    }
  };

  /* =========================================================
     Loading
  ========================================================= */

  if (loading) {
    return (
      <main className={styles.page}>
        <div className={styles.loading}>
          Loading plans...
        </div>
      </main>
    );
  }

  /* =========================================================
     Fatal Error
  ========================================================= */

  if (error && pricing.length === 0) {
    return (
      <main className={styles.page}>
        <div className={styles.error}>
          {error}
        </div>
      </main>
    );
  }

  /* =========================================================
     UI
  ========================================================= */

  return (
    <main className={styles.page}>

      <section className={styles.header}>

        <p className={styles.eyebrow}>
          ResumeOptimizer
        </p>

        <h1>
          Choose your plan
        </h1>

        <p className={styles.subtitle}>
          Same Resume. Smarter Words.
        </p>

        <div className={styles.toggle}>

          <button
            type="button"
            className={
              interval === "monthly"
                ? styles.activeToggle
                : styles.toggleButton
            }
            onClick={() => {
              setInterval("monthly");
              setCheckoutMessage(null);
              setError(null);
            }}
          >
            Monthly
          </button>

          <button
            type="button"
            className={
              interval === "yearly"
                ? styles.activeToggle
                : styles.toggleButton
            }
            onClick={() => {
              setInterval("yearly");
              setCheckoutMessage(null);
              setError(null);
            }}
          >
            Yearly
          </button>

        </div>

      </section>

      {checkoutMessage && (
        <div className={styles.notice}>
          <strong>
            Payments aren't available yet
          </strong>

          <span>
            {checkoutMessage}
          </span>
        </div>
      )}

      {error && (
        <div className={styles.inlineError}>
          {error}
        </div>
      )}

      <section className={styles.grid}>

        {pricing.map((plan) => {

          const price =
            interval === "monthly"
              ? plan.monthly_price
              : plan.yearly_price;

          const unavailable =
            interval === "yearly" &&
            plan.yearly_price === null;

          const isCheckout =
            checkoutPlan ===
            plan.plan_code;

          return (
            <article
              key={plan.id}
              className={styles.card}
            >

              <div>

                <h2>
                  {plan.plan_name}
                </h2>

                {plan.description && (
                  <p
                    className={
                      styles.description
                    }
                  >
                    {plan.description}
                  </p>
                )}

              </div>

              <div className={styles.price}>

                {unavailable ? (
                  <span>
                    Not available
                  </span>
                ) : (
                  <>
                    <strong>
                      {plan.currency_code}{" "}
                      {price}
                    </strong>

                    <span>
                      /
                      {interval === "monthly"
                        ? "month"
                        : "year"}
                    </span>
                  </>
                )}

              </div>

              <div className={styles.limit}>
                {plan.monthly_optimizations}{" "}
                optimizations / month
              </div>

              <button
                type="button"
                className={styles.checkoutButton}
                disabled={
                  unavailable ||
                  checkoutPlan !== null
                }
                onClick={() =>
                  void handleCheckout(plan)
                }
              >
                {isCheckout
                  ? "Preparing checkout..."
                  : "Choose plan"}
              </button>

            </article>
          );
        })}

      </section>

    </main>
  );
};

export default PricingPage;