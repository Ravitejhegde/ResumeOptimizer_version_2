export interface Plan {
  id: string;
  code: string;
  name: string;
  description: string | null;
  active: boolean;
}

export interface Pricing {
  id: string;
  plan_code: string;
  plan_name: string;
  description: string | null;
  country_code: string;
  currency_code: string;
  monthly_price: number;
  yearly_price: number | null;
  monthly_optimizations: number;
  payment_provider: string;
  active: boolean;
}

export type BillingInterval = "monthly" | "yearly";

export interface CheckoutRequest {
  email: string;
  name: string;
  country: string;
  plan: string;
  interval: BillingInterval;
  provider: string;
  success_url: string;
  cancel_url: string;
}

export interface CheckoutResponse {
  order_id: string;
  customer_id: string;
  checkout_session_id: string;
  checkout_url: string;
  provider: string;
  country: string;
  plan: string;
  interval: BillingInterval;
  price: number;
  currency: string;
  trial_days: number;
  features: string[];
}