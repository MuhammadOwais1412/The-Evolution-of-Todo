import { betterAuth } from "better-auth";
import { Pool } from "pg";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || "change-me-in-production",
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",

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
