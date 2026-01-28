"use client";

<<<<<<< HEAD
import { useState, useEffect, useRef } from "react";
=======
import { useState } from "react";
>>>>>>> 003-frontend-better-auth
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/auth-context";

export default function LoginPage() {
  const router = useRouter();
<<<<<<< HEAD
  const { login, isAuthenticated, isLoading: authLoading } = useAuth();
=======
  const { login, isLoading: authLoading } = useAuth();
>>>>>>> 003-frontend-better-auth
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
<<<<<<< HEAD
  const [showForm, setShowForm] = useState(false);
  const hasRedirected = useRef(false);

  // Check if user is already authenticated and redirect to dashboard
  useEffect(() => {
    if (!authLoading && isAuthenticated && !hasRedirected.current) {
      hasRedirected.current = true;
      router.push("/tasks");
    } else if (!authLoading && !isAuthenticated) {
      setShowForm(true);
    }
  }, [authLoading, isAuthenticated, router]);

  // Show loading state while checking authentication
  if (authLoading || !showForm) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }
=======
>>>>>>> 003-frontend-better-auth

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      await login(email, password);
      // Redirect to tasks dashboard after successful login
      router.push("/tasks");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-md">
        <h1 className="text-2xl font-bold mb-6 text-center">Log In</h1>

        {error && (
          <div className="mb-4 p-3 bg-red-50 text-red-700 rounded border border-red-200">
            {error}
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label
              htmlFor="email"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Email
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="you@example.com"
              required
              autoComplete="email"
              disabled={isLoading || authLoading}
            />
          </div>

          <div>
            <label
              htmlFor="password"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Enter your password"
              required
              autoComplete="current-password"
              disabled={isLoading || authLoading}
            />
          </div>

          <button
            type="submit"
            disabled={isLoading || authLoading}
            className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors min-h-[44px] touch-manipulation"
          >
            {isLoading || authLoading ? "Logging in..." : "Log In"}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-gray-600">
<<<<<<< HEAD
          Don{"'"}t have an account?{" "}
=======
          Don't have an account?{" "}
>>>>>>> 003-frontend-better-auth
          <Link href="/signup" className="text-blue-600 hover:text-blue-700 hover:underline">
            Sign up
          </Link>
        </p>
      </div>
    </div>
  );
}
