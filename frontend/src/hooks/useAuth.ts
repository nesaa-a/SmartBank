import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuthStore } from "../store/authStore";
import { authService } from "../services/authService";

export function useAuth() {
  const store = useAuthStore();
  const navigate = useNavigate();

  useEffect(() => {
    if (store.accessToken && !store.user) {
      authService.me().then(store.setUser).catch(() => store.logout());
    }
  }, [store.accessToken]);

  async function login(email: string, password: string) {
    const tokens = await authService.login({ email, password });
    store.setTokens(tokens.access_token, tokens.refresh_token);
    const user = await authService.me();
    store.setUser(user);
    navigate("/dashboard");
  }

  async function logout() {
    if (store.refreshToken) {
      await authService.logout(store.refreshToken).catch(() => {});
    }
    store.logout();
    navigate("/login");
  }

  return { user: store.user, login, logout, isAuthenticated: store.isAuthenticated() };
}
