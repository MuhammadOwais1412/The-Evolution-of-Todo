# Better Auth Database Setup

This guide explains how to set up the required database tables for Better Auth in your Neon PostgreSQL database.

## Overview

Better Auth requires specific database tables to store user accounts, sessions, OAuth credentials, and verification tokens. These tables are not automatically created in PostgreSQL, so we need to run migrations to set them up.

## Required Tables

The following tables will be created:
- `user`: Stores user account information (name, email, etc.)
- `account`: Stores OAuth provider credentials and tokens
- `session`: Stores authentication session information
- `verification`: Stores verification tokens (email verification, password reset, etc.)
- `jwks`: Stores JWT cryptographic keys (publicKey, privateKey) for JWT plugin

## Setup Instructions

### 1. Environment Variables

Make sure your `.env.local` file contains the database connection string:

```bash
DATABASE_URL=your_neon_database_connection_string
# or
NEON_DATABASE_URL=your_neon_database_connection_string
```

### 2. Run Database Migration

Use one of the following methods to create the required tables:

#### Method 1: Using npm scripts (recommended)

```bash
cd Phase-2-web-todo/frontend
npm run db:setup
```

This runs both the migration and verification scripts in sequence.

#### Method 2: Run scripts individually

```bash
cd Phase-2-web-todo/frontend
npm run migrate          # Create tables
npm run verify-tables    # Verify tables were created correctly
```

### 3. Alternative: Manual SQL Execution

If you prefer to run the SQL manually, you can execute the queries from `better_auth_postgresql_schema.sql` directly in your Neon database console.

## Scripts

### `npm run migrate`

This script:
- Connects to your PostgreSQL database
- Creates all required tables if they don't exist
- Sets up proper indexes for performance
- Creates triggers to automatically update timestamps
- Handles errors gracefully with rollbacks

### `npm run verify-tables`

This script:
- Checks if all required tables exist
- Verifies table structure and columns
- Reports on indexes and constraints
- Provides a detailed summary of the database state

### `npm run db:setup`

This convenience script runs both migrate and verify-tables in sequence.

## Troubleshooting

### Common Issues

1. **Connection Error**: Ensure your `DATABASE_URL` environment variable is correctly set with proper credentials and SSL settings.

2. **Permission Error**: Make sure your database user has permissions to create tables and indexes.

3. **Relation Does Not Exist Error**: This error occurs when Better Auth tries to access tables that don't exist yet. Run the migration script to resolve this.

### Verification Output

When running `npm run verify-tables`, you should see output similar to:

```
=== VERIFICATION SUMMARY ===
✅ user: Exists
✅ account: Exists
✅ session: Exists
✅ verification: Exists

=== FINAL STATUS ===
🎉 All required Better Auth tables exist in the database!
✅ Ready for authentication functionality
```

## Notes

- The migration script is idempotent, meaning you can run it multiple times safely
- All tables include proper foreign key relationships and cascading deletes
- Timestamps are automatically managed with triggers
- The setup works with both Neon and standard PostgreSQL databases