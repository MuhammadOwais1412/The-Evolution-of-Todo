import { createAuthClient } from "better-auth/react";
import { jwtClient } from "better-auth/client/plugins";

// For Vercel deployments, use consistent base URL to handle production properly
const getBaseURL = (): string => {
  // Prioritize environment variable in both client and server contexts
  if (process.env.NEXT_PUBLIC_BETTER_AUTH_URL) {
    return process.env.NEXT_PUBLIC_BETTER_AUTH_URL;
  }

  if (typeof window !== 'undefined') {
    // Fallback to current origin only if environment variable is not set
    return window.location.origin;
  }

  // On server, use environment variable or throw error in production
  if (process.env.NODE_ENV === 'production') {
    throw new Error('NEXT_PUBLIC_BETTER_AUTH_URL is required in production');
  }
  return "http://localhost:3000"; // Default for development
};

// Validate required environment variables in production
if (process.env.NODE_ENV === 'production' && !process.env.NEXT_PUBLIC_BETTER_AUTH_URL) {
  console.error('ERROR: NEXT_PUBLIC_BETTER_AUTH_URL is not set in environment variables.');
  if (typeof window !== 'undefined') {
    throw new Error('NEXT_PUBLIC_BETTER_AUTH_URL is required in production');
  }
}

export const authClient = createAuthClient({
  baseURL: getBaseURL(),
  plugins: [jwtClient()],
});