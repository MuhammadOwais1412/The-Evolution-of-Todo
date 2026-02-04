import { betterAuth } from "better-auth";
import { Pool } from "pg";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  secret: (() => {
    if (!process.env.BETTER_AUTH_SECRET) {
      console.error('BETTER_AUTH_SECRET is not set in environment variables');
      throw new Error('BETTER_AUTH_SECRET is required in production');
    }
    return process.env.BETTER_AUTH_SECRET;
  })(),
  baseURL: (() => {
    if (!process.env.NEXT_PUBLIC_BETTER_AUTH_URL && !process.env.BETTER_AUTH_URL) {
      console.error('BETTER_AUTH_URL or NEXT_PUBLIC_BETTER_AUTH_URL is not set in environment variables');
      throw new Error('BETTER_AUTH_URL is required in production');
    }
    return process.env.NEXT_PUBLIC_BETTER_AUTH_URL || process.env.BETTER_AUTH_URL;
  })(),

  // Enable trustHost to handle serverless environments properly
  trustHost: true,

  // PostgreSQL database connection using direct Pool connection
  database: new Pool({
    connectionString: process.env.DATABASE_URL || process.env.NEON_DATABASE_URL,
  }),

  // Map field names to our camelCase columns
  user: {
    fields: {
      emailVerified: "emailVerified",
      createdAt: "createdAt",
      updatedAt: "updatedAt"
    }
  },
  account: {
    fields: {
      userId: "userId",
      accountId: "accountId",
      providerId: "providerId",
      accessToken: "accessToken",
      refreshToken: "refreshToken",
      idToken: "idToken",
      accessTokenExpiresAt: "accessTokenExpiresAt",
      refreshTokenExpiresAt: "refreshTokenExpiresAt",
      createdAt: "createdAt",
      updatedAt: "updatedAt"
    }
  },
  session: {
    fields: {
      userId: "userId",
      expiresAt: "expiresAt",
      createdAt: "createdAt",
      updatedAt: "updatedAt",
      ipAddress: "ipAddress",
      userAgent: "userAgent"
    }
  },
  verification: {
    fields: {
      expiresAt: "expiresAt",
      createdAt: "createdAt",
      updatedAt: "updatedAt"
    }
  },

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