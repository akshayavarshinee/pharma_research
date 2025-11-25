"""
Quick fix for database schema - adds missing columns to queries table
"""
import os
from dotenv import load_dotenv
import psycopg2

# Load environment variables
load_dotenv()

# Get database URL
database_url = os.getenv('DATABASE_URL')

if not database_url:
    print("❌ DATABASE_URL not found in .env file")
    exit(1)

print("Connecting to database...")

try:
    # Connect to database
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    print("Adding status tracking columns...")
    
    # Add columns if they don't exist
    cursor.execute("""
        ALTER TABLE queries 
        ADD COLUMN IF NOT EXISTS status VARCHAR DEFAULT 'pending'
    """)
    
    cursor.execute("""
        ALTER TABLE queries 
        ADD COLUMN IF NOT EXISTS started_at TIMESTAMP
    """)
    
    cursor.execute("""
        ALTER TABLE queries 
        ADD COLUMN IF NOT EXISTS completed_at TIMESTAMP
    """)
    
    cursor.execute("""
        ALTER TABLE queries 
        ADD COLUMN IF NOT EXISTS error_message TEXT
    """)
    
    # Update existing queries
    cursor.execute("""
        UPDATE queries 
        SET status = 'completed' 
        WHERE id IN (SELECT query_id FROM reports)
        AND (status IS NULL OR status = '')
    """)
    
    # Commit changes
    conn.commit()
    
    print("✅ Database schema updated successfully!")
    print("   Added columns: status, started_at, completed_at, error_message")
    
    # Show current schema
    cursor.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_name = 'queries'
        ORDER BY ordinal_position
    """)
    
    print("\n📊 Current queries table schema:")
    for row in cursor.fetchall():
        print(f"   - {row[0]}: {row[1]} (nullable: {row[2]}, default: {row[3]})")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)
