

import type {
  CheckoutRequest,
  CheckoutResponse,
  Plan,
  Pricing,
} from "../types/billing";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ??
  "http://127.0.0.1:8000";

/* =========================================================
   Headers
========================================================= */

const getHeaders = (): HeadersInit => {
  const token =
    localStorage.getItem("access_token");

  return {
    "Content-Type": "application/json",
    ...(token
      ? {
          Authorization: `Bearer ${token}`,
        }
      : {}),
  };
};

/* =========================================================
   Response Handling
========================================================= */

const handleResponse = async <T>(
  response: Response,
): Promise<T> => {
  if (!response.ok) {
    let message =
      `Billing request failed with status ${response.status}.`;

    try {
      const data = await response.json();

      if (
        typeof data?.detail === "string"
      ) {
        message = data.detail;
      } else if (
        Array.isArray(data?.detail)
      ) {
        message = data.detail
          .map(
            (item: {
              msg?: string;
            }) => item.msg ?? "Invalid request.",
          )
          .join(", ");
      }
    } catch {
      // Keep default message.
    }

    throw new Error(message);
  }

  return response.json() as Promise<T>;
};

/* =========================================================
   Plans
========================================================= */

export const getPlans =
  async (): Promise<Plan[]> => {
    const response = await fetch(
      `${API_BASE_URL}/billing/plans`,
      {
        method: "GET",
        headers: getHeaders(),
      },
    );

    return handleResponse<Plan[]>(
      response,
    );
  };

/* =========================================================
   Pricing
========================================================= */

export const getPricing = async (
  country: string,
): Promise<Pricing[]> => {
  const response = await fetch(
    `${API_BASE_URL}/billing/pricing?country=${encodeURIComponent(
      country.toUpperCase(),
    )}`,
    {
      method: "GET",
      headers: getHeaders(),
    },
  );

  return handleResponse<Pricing[]>(
    response,
  );
};

/* =========================================================
   Checkout
========================================================= */

export const createCheckout =
  async (
    request: CheckoutRequest,
  ): Promise<CheckoutResponse> => {
    const response = await fetch(
      `${API_BASE_URL}/billing/checkout`,
      {
        method: "POST",
        headers: getHeaders(),
        body: JSON.stringify(request),
      },
    );

    return handleResponse<CheckoutResponse>(
      response,
    );
  };