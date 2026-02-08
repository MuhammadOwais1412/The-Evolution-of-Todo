// Better Auth PostgreSQL Schema Setup for Neon
// This script creates the required tables for Better Auth in a Neon PostgreSQL database

const { Client } = require('pg');

async function setupBetterAuthSchema() {
  const client = new Client({
    connectionString: process.env.DATABASE_URL || process.env.NEON_DATABASE_URL,
  });

  await client.connect();

  try {
    // Begin transaction
    await client.query('BEGIN');

    // User table
    await client.query(`
      CREATE TABLE IF NOT EXISTS "user" (
          id TEXT PRIMARY KEY,
          name TEXT NOT NULL,
          email TEXT NOT NULL UNIQUE,
          email_verified BOOLEAN DEFAULT FALSE NOT NULL,
          image TEXT,
          created_at TIMESTAMP DEFAULT NOW() NOT NULL,
          updated_at TIMESTAMP DEFAULT NOW() NOT NULL
      );
    `);

    // Account table (for OAuth providers and password storage)
    await client.query(`
      CREATE TABLE IF NOT EXISTS account (
          id TEXT PRIMARY KEY,
          account_id TEXT NOT NULL,
          provider_id TEXT NOT NULL,
          user_id TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
          access_token TEXT,
          refresh_token TEXT,
          id_token TEXT,
          access_token_expires_at TIMESTAMP,
          refresh_token_expires_at TIMESTAMP,
          scope TEXT,
          password TEXT,
          created_at TIMESTAMP DEFAULT NOW() NOT NULL,
          updated_at TIMESTAMP DEFAULT NOW() NOT NULL
      );
    `);

    // Index for account table
    await client.query(`
      CREATE INDEX IF NOT EXISTS account_userId_idx ON account(user_id);
    `);

    // Session table
    await client.query(`
      CREATE TABLE IF NOT EXISTS session (
          id TEXT PRIMARY KEY,
          expires_at TIMESTAMP NOT NULL,
          token TEXT NOT NULL UNIQUE,
          created_at TIMESTAMP DEFAULT NOW() NOT NULL,
          updated_at TIMESTAMP DEFAULT NOW() NOT NULL,
          ip_address TEXT,
          user_agent TEXT,
          user_id TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE
      );
    `);

    // Index for session table
    await client.query(`
      CREATE INDEX IF NOT EXISTS session_userId_idx ON session(user_id);
    `);

    // Verification table (for email verification, password reset, etc.)
    await client.query(`
      CREATE TABLE IF NOT EXISTS verification (
          id TEXT PRIMARY KEY,
          identifier TEXT NOT NULL,
          value TEXT NOT NULL,
          expires_at TIMESTAMP NOT NULL,
          created_at TIMESTAMP DEFAULT NOW() NOT NULL,
          updated_at TIMESTAMP DEFAULT NOW() NOT NULL
      );
    `);

    // Index for verification table
    await client.query(`
      CREATE INDEX IF NOT EXISTS verification_identifier_idx ON verification(identifier);
    `);

    // Trigger function to automatically update the updated_at timestamp
    await client.query(`
      CREATE OR REPLACE FUNCTION update_updated_at_column()
      RETURNS TRIGGER AS $$
      BEGIN
          NEW.updated_at = NOW();
          RETURN NEW;
      END;
      $$ language 'plpgsql';
    `);

    // Apply triggers to all tables that have updated_at column
    await client.query(`
      CREATE TRIGGER update_user_updated_at BEFORE UPDATE ON "user" FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    `);

    await client.query(`
      CREATE TRIGGER update_account_updated_at BEFORE UPDATE ON account FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    `);

    await client.query(`
      CREATE TRIGGER update_session_updated_at BEFORE UPDATE ON session FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    `);

    await client.query(`
      CREATE TRIGGER update_verification_updated_at BEFORE UPDATE ON verification FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    `);

    // Commit transaction
    await client.query('COMMIT');
    console.log('Better Auth schema created successfully!');
  } catch (err) {
    await client.query('ROLLBACK');
    console.error('Error setting up Better Auth schema:', err);
    throw err;
  } finally {
    await client.end();
  }
}

module.exports = { setupBetterAuthSchema };

// If running this script directly
if (require.main === module) {
  setupBetterAuthSchema()
    .catch(err => {
      console.error('Failed to setup Better Auth schema:', err);
      process.exit(1);
    });
}