import { createAuthClient } from "better-auth/react";
import { jwtClient } from "better-auth/client/plugins";

// Validate required environment variables in development
if (typeof window !== 'undefined' && process.env.NODE_ENV === 'production') {
  if (!process.env.NEXT_PUBLIC_BETTER_AUTH_URL) {
    console.error('NEXT_PUBLIC_BETTER_AUTH_URL is not set in environment variables');
  }
}

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "",
  plugins: [jwtClient()],
});
