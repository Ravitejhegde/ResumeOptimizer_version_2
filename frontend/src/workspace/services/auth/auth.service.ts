import api from "../api/client";

/* =========================================================
   Types
   ========================================================= */

export interface RegisterRequest {
  name: string;
  email: string;
  password: string;
}

export interface RegisterResponse {
  message: string;
  email: string;
  verified: boolean;
}

export interface VerifyEmailRequest {
  email: string;
  otp: string;
}

export interface VerifyEmailResponse {
  message: string;
  email: string;
  verified: boolean;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string | null;
  token_type: string;
}

export interface CurrentUser {
  id: string;
  name: string;
  email: string;
  verified: boolean;
}

/* =========================================================
   Register
   ========================================================= */

export async function register(
  data: RegisterRequest,
): Promise<RegisterResponse> {
  const response = await api.post<RegisterResponse>(
    "/auth/register",
    data,
  );

  return response.data;
}

/* =========================================================
   Email Verification
   ========================================================= */

export async function verifyEmail(
  data: VerifyEmailRequest,
): Promise<VerifyEmailResponse> {
  const response = await api.post<VerifyEmailResponse>(
    "/auth/verify-email",
    data,
  );

  return response.data;
}

/* =========================================================
   Login
   ========================================================= */

export async function login(
  credentials: LoginRequest,
): Promise<AuthResponse> {
  const response = await api.post<AuthResponse>(
    "/auth/login",
    credentials,
  );

  const tokens = response.data;

  localStorage.setItem(
    "access_token",
    tokens.access_token,
  );

  if (tokens.refresh_token) {
    localStorage.setItem(
      "refresh_token",
      tokens.refresh_token,
    );
  } else {
    localStorage.removeItem("refresh_token");
  }

  return tokens;
}

/* =========================================================
   Current User
   ========================================================= */

export async function getCurrentUser(): Promise<CurrentUser> {
  const response = await api.get<CurrentUser>(
    "/users/me",
  );

  return response.data;
}

/* =========================================================
   Logout
   ========================================================= */

export function logout(): void {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
}

/* =========================================================
   Authentication Helpers
   ========================================================= */

export function getAccessToken(): string | null {
  return localStorage.getItem("access_token");
}

export function isAuthenticated(): boolean {
  return Boolean(getAccessToken());
}