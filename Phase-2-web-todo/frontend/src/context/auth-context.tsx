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
  isTokenReady: boolean;  // Indicates if JWT token is synchronized with API client
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
  const [isTokenReady, setIsTokenReady] = useState<boolean>(false); // Track if JWT token is ready

  const isAuthenticated = !!session?.user;
  const userId = session?.user?.id ?? null;
  const user = (session?.user as User | undefined) ?? null;

  const refreshSession = async () => {
    setError(null);
    console.log('Refreshing session...', {
      timestamp: new Date().toISOString()
    });
    await refetch();
    console.log('Session refresh completed', {
      hasSession: !!session?.user,
      timestamp: new Date().toISOString()
    });
  };

  // Keep API client JWT in sync with auth state.
  useEffect(() => {
    let cancelled = false;

    async function syncToken() {
      console.log('Syncing token with API client:', {
        hasUser: !!session?.user,
        sessionId: session?.session?.id,
        timestamp: new Date().toISOString()
      });

      if (!session?.user) {
        console.log('No user session, clearing token');
        setToken(null);
        setIsTokenReady(false);
        return;
      }

      const { data, error: tokenError } = await authClient.token();
      if (cancelled) return;

      console.log('Token sync response:', {
        hasData: !!data?.token,
        hasError: !!tokenError,
        error: tokenError,
        timestamp: new Date().toISOString()
      });

      if (tokenError || !data?.token) {
        console.error('Token sync failed:', tokenError);
        setToken(null);
        setIsTokenReady(false);
        return;
      }

      setToken(data.token);
      setIsTokenReady(true);
      console.log('Token sync completed successfully');
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

    // Log login request details
    console.log('Auth client signIn request:', {
      method: 'signIn.email',
      email,
      timestamp: new Date().toISOString()
    });

    const { error: signInError } = await authClient.signIn.email({
      email,
      password,
      rememberMe: true,
    });

    // Log response details
    console.log('Auth client signIn response:', {
      hasError: !!signInError,
      error: signInError,
      timestamp: new Date().toISOString()
    });

    if (signInError) {
      const message = signInError.message || "Login failed";
      setError(message);
      console.error('Sign in error occurred:', signInError);
      throw new Error(message);
    }

    console.log('Sign in successful, refreshing session...');
    await refreshSession();
    console.log('Session refreshed successfully');
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
      isTokenReady,
      error,
      login,
      signup,
      logout,
      refreshSession,
    }),
    [isAuthenticated, userId, user, isPending, isTokenReady, error]
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
