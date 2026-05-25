import { api } from "./api";
import type { LoginRequest, RegisterRequest, TokenResponse, User } from "../types/auth";

export const authService = {
  async login(data: LoginRequest): Promise<TokenResponse> {
    const res = await api.post<TokenResponse>("/auth/login", data);
    return res.data;
  },

  async register(data: RegisterRequest): Promise<User> {
    const res = await api.post<User>("/auth/register", data);
    return res.data;
  },

  async me(): Promise<User> {
    const res = await api.get<User>("/auth/me");
    return res.data;
  },

  async logout(refresh_token: string): Promise<void> {
    await api.post("/auth/logout", { refresh_token });
  },
};
