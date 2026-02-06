/**
 * Better Auth Database Migration Script
 * Creates required tables for Better Auth in Neon PostgreSQL database
 */

import { Client } from 'pg';
import * as dotenv from 'dotenv';

// Load environment variables from .env.local file
dotenv.config({ path: '.env.local' });

async function runMigration() {
  const connectionString = process.env.DATABASE_URL || process.env.NEON_DATABASE_URL;

  if (!connectionString) {
    throw new Error('DATABASE_URL or NEON_DATABASE_URL environment variable is required');
  }

  const client = new Client({
    connectionString,
  });

  try {
    console.log('Connecting to database...');
    await client.connect();
    console.log('Connected to database successfully.');

    // Begin transaction
    await client.query('BEGIN');
    console.log('Starting migration...');

    // Check if tables already exist with camelCase columns
    const userTableCheck = await client.query(`
      SELECT column_name
      FROM information_schema.columns
      WHERE table_name = 'user' AND column_name = 'emailVerified'
    `);

    // Check if jwks table exists
    const jwksTableCheck = await client.query(`
      SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_name = 'jwks'
      ) as exists;
    `);

    const jwksExists = jwksTableCheck.rows[0].exists;

    if (userTableCheck.rows.length === 0) {
      console.log('Creating tables with camelCase columns...');

      // User table
      await client.query(`
        CREATE TABLE IF NOT EXISTS "user" (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            "emailVerified" BOOLEAN DEFAULT FALSE NOT NULL,
            image TEXT,
            "createdAt" TIMESTAMP DEFAULT NOW() NOT NULL,
            "updatedAt" TIMESTAMP DEFAULT NOW() NOT NULL
        );
      `);
      console.log('✓ User table created/verified');

      // Account table (for OAuth providers and password storage)
      await client.query(`
        CREATE TABLE IF NOT EXISTS account (
            id TEXT PRIMARY KEY,
            "accountId" TEXT NOT NULL,
            "providerId" TEXT NOT NULL,
            "userId" TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
            "accessToken" TEXT,
            "refreshToken" TEXT,
            "idToken" TEXT,
            "accessTokenExpiresAt" TIMESTAMP,
            "refreshTokenExpiresAt" TIMESTAMP,
            scope TEXT,
            password TEXT,
            "createdAt" TIMESTAMP DEFAULT NOW() NOT NULL,
            "updatedAt" TIMESTAMP DEFAULT NOW() NOT NULL
        );
      `);
      console.log('✓ Account table created/verified');

      // Index for account table
      await client.query(`
        CREATE INDEX IF NOT EXISTS account_userId_idx ON account("userId");
      `);

      // Session table
      await client.query(`
        CREATE TABLE IF NOT EXISTS session (
            id TEXT PRIMARY KEY,
            "expiresAt" TIMESTAMP NOT NULL,
            token TEXT NOT NULL UNIQUE,
            "createdAt" TIMESTAMP DEFAULT NOW() NOT NULL,
            "updatedAt" TIMESTAMP DEFAULT NOW() NOT NULL,
            "ipAddress" TEXT,
            "userAgent" TEXT,
            "userId" TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE
        );
      `);
      console.log('✓ Session table created/verified');

      // Index for session table
      await client.query(`
        CREATE INDEX IF NOT EXISTS session_userId_idx ON session("userId");
      `);

      // Verification table (for email verification, password reset, etc.)
      await client.query(`
        CREATE TABLE IF NOT EXISTS verification (
            id TEXT PRIMARY KEY,
            identifier TEXT NOT NULL,
            value TEXT NOT NULL,
            "expiresAt" TIMESTAMP NOT NULL,
            "createdAt" TIMESTAMP DEFAULT NOW() NOT NULL,
            "updatedAt" TIMESTAMP DEFAULT NOW() NOT NULL
        );
      `);
      console.log('✓ Verification table created/verified');

      // Index for verification table
      await client.query(`
        CREATE INDEX IF NOT EXISTS verification_identifier_idx ON verification(identifier);
      `);

      // Trigger function to automatically update the updatedAt timestamp
      await client.query(`
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW."updatedAt" = NOW();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
      `);

      // Apply triggers to all tables that have updatedAt column
      await client.query(`
        DROP TRIGGER IF EXISTS update_user_updated_at ON "user";
        CREATE TRIGGER update_user_updated_at BEFORE UPDATE ON "user" FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
      `);

      await client.query(`
        DROP TRIGGER IF EXISTS update_account_updated_at ON account;
        CREATE TRIGGER update_account_updated_at BEFORE UPDATE ON account FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
      `);

      await client.query(`
        DROP TRIGGER IF EXISTS update_session_updated_at ON session;
        CREATE TRIGGER update_session_updated_at BEFORE UPDATE ON session FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
      `);

      await client.query(`
        DROP TRIGGER IF EXISTS update_verification_updated_at ON verification;
        CREATE TRIGGER update_verification_updated_at BEFORE UPDATE ON verification FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
      `);

      // JWKS table (for JWT cryptographic keys) - does not use updatedAt trigger
      await client.query(`
        CREATE TABLE IF NOT EXISTS jwks (
            id TEXT PRIMARY KEY,
            "publicKey" TEXT NOT NULL,
            "privateKey" TEXT NOT NULL,
            "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
      `);
      console.log('✓ JWKS table created/verified');

    } else {
      console.log('Tables with camelCase columns already exist, skipping creation of main tables.');
    }

    // Create JWKS table if it doesn't exist (needed for JWT plugin)
    if (!jwksExists) {
      console.log('Creating JWKS table for JWT plugin...');

      // JWKS table (for JWT cryptographic keys)
      await client.query(`
        CREATE TABLE IF NOT EXISTS jwks (
            id TEXT PRIMARY KEY,
            "publicKey" TEXT NOT NULL,
            "privateKey" TEXT NOT NULL,
            "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
      `);
      console.log('✓ JWKS table created');

    } else {
      console.log('JWKS table already exists, ensuring correct schema...');

      // Add missing required columns if they don't exist
      const requiredColumns = [
        { name: 'id', definition: 'TEXT PRIMARY KEY' },
        { name: 'publicKey', definition: 'TEXT NOT NULL' },
        { name: 'privateKey', definition: 'TEXT NOT NULL' },
        { name: 'createdAt', definition: 'TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP' }
      ];

      for (const col of requiredColumns) {
        const columnCheck = await client.query(`
          SELECT column_name
          FROM information_schema.columns
          WHERE table_name = 'jwks' AND column_name = $1
        `, [col.name]);

        if (columnCheck.rows.length === 0) {
          if (col.name === 'id') {
            // Special handling for id column if it doesn't exist
            await client.query(`
              ALTER TABLE jwks ADD COLUMN "${col.name}" ${col.definition};
            `);
          } else {
            await client.query(`
              ALTER TABLE jwks ADD COLUMN "${col.name}" ${col.definition};
            `);
          }
          console.log(`✓ Added missing column: ${col.name}`);
        } else {
          console.log(`✓ Column ${col.name} already exists`);
        }
      }

      // Drop old JWKS-specific columns that are not needed by Better Auth
      const oldColumns = ['kid', 'use', 'alg', 'kty', 'crv', 'x', 'y', 'n', 'e', 'd', 'p', 'q', 'dp', 'dq', 'qi', 'updatedAt'];

      for (const col of oldColumns) {
        const columnCheck = await client.query(`
          SELECT column_name
          FROM information_schema.columns
          WHERE table_name = 'jwks' AND column_name = $1
        `, [col]);

        if (columnCheck.rows.length > 0) {
          await client.query(`
            ALTER TABLE jwks DROP COLUMN IF EXISTS "${col}";
          `);
          console.log(`✓ Cleaned up old column: ${col}`);
        }
      }

      console.log('✓ JWKS table schema is up to date');
    }

    // Commit transaction
    await client.query('COMMIT');
    console.log('✅ Migration completed successfully!');
  } catch (error) {
    console.error('❌ Migration failed, rolling back:', error);
    await client.query('ROLLBACK');
    throw error;
  } finally {
    await client.end();
    console.log('Database connection closed.');
  }
}

// Run migration if this script is executed directly
if (require.main === module) {
  runMigration()
    .then(() => {
      console.log('Migration process finished.');
      process.exit(0);
    })
    .catch((error) => {
      console.error('Migration process failed:', error);
      process.exit(1);
    });
}

export default runMigration;