-- Add status tracking columns to queries table
-- Run this with: psql -U postgres -d pharma_research -f fix_schema.sql

-- Add status column
ALTER TABLE queries ADD COLUMN IF NOT EXISTS status VARCHAR DEFAULT 'pending';

-- Add timestamp columns
ALTER TABLE queries ADD COLUMN IF NOT EXISTS started_at TIMESTAMP;
ALTER TABLE queries ADD COLUMN IF NOT EXISTS completed_at TIMESTAMP;

-- Add error message column
ALTER TABLE queries ADD COLUMN IF NOT EXISTS error_message TEXT;

-- Update existing queries that have reports to 'completed' status
UPDATE queries 
SET status = 'completed' 
WHERE id IN (SELECT query_id FROM reports)
AND status IS NULL;

-- Show the updated schema
\d queries
