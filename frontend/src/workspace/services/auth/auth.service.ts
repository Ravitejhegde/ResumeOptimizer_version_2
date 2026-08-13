import api from "../api/client";

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
}

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
  }

  return tokens;
}

export async function getCurrentUser(): Promise<CurrentUser> {
  const response = await api.get<CurrentUser>(
    "/users/me",
  );

  return response.data;
}

export function logout(): void {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
}

export function getAccessToken(): string | null {
  return localStorage.getItem("access_token");
}

export function isAuthenticated(): boolean {
  return Boolean(getAccessToken());
}