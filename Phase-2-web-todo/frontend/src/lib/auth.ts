import { betterAuth } from "better-auth";
import { memoryAdapter } from "better-auth/adapters/memory";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || "change-me-in-production",
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",

  // Dev-only persistence. Replace with a real adapter before production.
  database: memoryAdapter({}),

  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8,
    // Keep signup and login separate (matches current UX redirect to /login).
    autoSignIn: false,
  },

  plugins: [
    jwt(),
  ],
});

export type Session = typeof auth.$Infer.Session;
