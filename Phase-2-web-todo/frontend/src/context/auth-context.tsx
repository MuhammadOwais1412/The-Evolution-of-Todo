"use client";

import { createContext, useContext, useEffect, useMemo, ReactNode, useState } from "react";
import { authClient } from "@/lib/auth-client";
import { setToken } from "@/lib/api-client";

interface User {
  id: string;
  email: string;
  name?: string | null;
}

interface AuthContextType {
  isAuthenticated: boolean;
  userId: string | null;
  user: User | null;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string, name?: string) => Promise<void>;
  logout: () => Promise<void>;
  refreshSession: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const { data: session, error: sessionError, isPending, refetch } = authClient.useSession();

  const [error, setError] = useState<string | null>(null);

  const isAuthenticated = !!session?.user;
  const userId = session?.user?.id ?? null;
  const user = (session?.user as User | undefined) ?? null;

  const refreshSession = async () => {
    setError(null);
    await refetch();
  };

  // Keep API client JWT in sync with auth state.
  useEffect(() => {
    let cancelled = false;

    async function syncToken() {
      if (!session?.user) {
        setToken(null);
        return;
      }

      const { data, error: tokenError } = await authClient.token();
      if (cancelled) return;

      if (tokenError || !data?.token) {
        setToken(null);
        return;
      }

      setToken(data.token);
    }

    void syncToken();

    return () => {
      cancelled = true;
    };
  }, [session?.user]);

  // Mirror Better Auth session error into our context error.
  useEffect(() => {
    if (!sessionError) return;
    const message =
      sessionError instanceof Error
        ? sessionError.message
        : "Authentication error";
    setError(message);
  }, [sessionError]);

  const login = async (email: string, password: string) => {
    setError(null);

    const { error: signInError } = await authClient.signIn.email({
      email,
      password,
      rememberMe: true,
    });

    if (signInError) {
      const message = signInError.message || "Login failed";
      setError(message);
      throw new Error(message);
    }

    await refreshSession();
  };

  const signup = async (email: string, password: string, name?: string) => {
    setError(null);

    const { error: signUpError } = await authClient.signUp.email({
      email,
      password,
      name: name || email.split('@')[0], // Use email prefix as name if not provided
    });

    if (signUpError) {
      const message = signUpError.message || "Signup failed";
      setError(message);
      throw new Error(message);
    }

    // If autoSignIn is enabled later, refreshSession will synchronize token.
    await refreshSession();
  };

  const logout = async () => {
    try {
      await authClient.signOut();
    } finally {
      setToken(null);
      await refreshSession();
    }
  };

  const value = useMemo<AuthContextType>(
    () => ({
      isAuthenticated,
      userId,
      user,
      isLoading: isPending,
      error,
      login,
      signup,
      logout,
      refreshSession,
    }),
    [isAuthenticated, userId, user, isPending, error]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
