/**
 * Better Auth Database Verification Script
 * Checks if all required tables exist with correct structure in Neon PostgreSQL database
 */

import { Client } from 'pg';
import * as dotenv from 'dotenv';

// Load environment variables from .env.local file
dotenv.config({ path: '.env.local' });

interface TableInfo {
  tableName: string;
  exists: boolean;
  columns?: Array<{ name: string; type: string; nullable: boolean; hasDefault: boolean }>;
  indexes?: Array<{ indexName: string; definition: string }>;
  foreignKeys?: Array<{ constraintName: string; definition: string }>;
}

async function verifyTables(): Promise<void> {
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
    console.log('Connected to database successfully.\n');

    // List of tables to verify
    const tablesToCheck = ['user', 'account', 'session', 'verification', 'jwks'];
    const verificationResults: TableInfo[] = [];

    for (const tableName of tablesToCheck) {
      console.log(`Checking table: ${tableName}`);

      // Check if table exists
      const tableExistsResult = await client.query(
        `SELECT EXISTS (
          SELECT FROM information_schema.tables
          WHERE table_schema = 'public'
          AND table_name = $1
        ) as exists;`,
        [tableName]
      );

      const exists = tableExistsResult.rows[0].exists;

      if (!exists) {
        console.log(`❌ Table '${tableName}' does not exist\n`);
        verificationResults.push({ tableName, exists: false });
        continue;
      }

      console.log(`✅ Table '${tableName}' exists`);

      // Get column information
      const columnsResult = await client.query(
        `SELECT column_name as name, data_type as type, is_nullable::boolean as nullable,
                column_default IS NOT NULL as has_default
         FROM information_schema.columns
         WHERE table_name = $1
         ORDER BY ordinal_position;`,
        [tableName]
      );

      const columns = columnsResult.rows.map(col => ({
        name: col.name,
        type: col.type,
        nullable: col.nullable === 'YES',
        hasDefault: col.has_default
      }));

      // Get index information
      const indexesResult = await client.query(
        `SELECT indexname as index_name, indexdef as definition
         FROM pg_indexes
         WHERE tablename = $1;`,
        [tableName]
      );

      const indexes = indexesResult.rows.map(idx => ({
        indexName: idx.index_name,
        definition: idx.definition
      }));

      // Get foreign key constraints
      const foreignKeysResult = await client.query(
        `SELECT tc.constraint_name,
                tc.table_name,
                kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name,
                rc.update_rule,
                rc.delete_rule
         FROM information_schema.table_constraints tc
         JOIN information_schema.key_column_usage kcu
           ON tc.constraint_name = kcu.constraint_name
         JOIN information_schema.constraint_column_usage ccu
           ON ccu.constraint_name = tc.constraint_name
         JOIN information_schema.referential_constraints rc
           ON tc.constraint_name = rc.constraint_name
         WHERE tc.constraint_type = 'FOREIGN KEY'
         AND tc.table_name = $1;`,
        [tableName]
      );

      const foreignKeys = foreignKeysResult.rows.map(fk => ({
        constraintName: fk.constraint_name,
        definition: `${fk.column_name} -> ${fk.foreign_table_name}.${fk.foreign_column_name}`
      }));

      console.log(`   Found ${columns.length} columns`);
      console.log(`   Found ${indexes.length} indexes`);
      console.log(`   Found ${foreignKeys.length} foreign key constraints\n`);

      verificationResults.push({
        tableName,
        exists: true,
        columns,
        indexes,
        foreignKeys
      });
    }

    // Summary
    console.log('=== VERIFICATION SUMMARY ===');
    let allTablesExist = true;
    let jwksColumnsValid = true;

    for (const result of verificationResults) {
      if (result.exists) {
        console.log(`✅ ${result.tableName}: Exists`);

        // Special check for jwks table columns
        if (result.tableName === 'jwks') {
          const requiredColumns = ['id', 'publicKey', 'privateKey', 'createdAt'];
          const existingColumns = result.columns?.map(col => col.name) || [];

          for (const requiredCol of requiredColumns) {
            if (!existingColumns.includes(requiredCol)) {
              console.log(`❌ jwks: Missing required column '${requiredCol}'`);
              jwksColumnsValid = false;
            }
          }

          if (jwksColumnsValid) {
            console.log('✅ jwks: All required columns present');
          }
        }
      } else {
        console.log(`❌ ${result.tableName}: Missing`);
        allTablesExist = false;
      }
    }

    console.log('\n=== DETAILED COLUMN INFORMATION ===');
    for (const result of verificationResults.filter(r => r.exists)) {
      console.log(`\n${result.tableName.toUpperCase()} TABLE COLUMNS:`);
      for (const col of result.columns!) {
        const nullableText = col.nullable ? 'NULL' : 'NOT NULL';
        const defaultText = col.hasDefault ? 'DEFAULT' : '';
        console.log(`  - ${col.name}: ${col.type} ${nullableText} ${defaultText}`.trim());
      }
    }

    // Final status
    console.log('\n=== FINAL STATUS ===');
    if (allTablesExist && jwksColumnsValid) {
      console.log('🎉 All required Better Auth tables exist in the database!');
      console.log('✅ Ready for authentication functionality');
    } else if (!allTablesExist) {
      console.log('❌ Some required tables are missing. Please run the migration script.');
    } else if (!jwksColumnsValid) {
      console.log('❌ JWKS table exists but is missing required columns. Please run the migration script.');
    }

  } catch (error) {
    console.error('❌ Verification failed:', error);
    throw error;
  } finally {
    await client.end();
    console.log('\nDatabase connection closed.');
  }
}

// Run verification if this script is executed directly
if (require.main === module) {
  verifyTables()
    .then(() => {
      console.log('\nVerification process completed.');
      process.exit(0);
    })
    .catch((error) => {
      console.error('\nVerification process failed:', error);
      process.exit(1);
    });
}

export default verifyTables;