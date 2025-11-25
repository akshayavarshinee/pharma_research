-- Migration script to add status tracking fields to queries table
-- Run this if you have existing data and don't want to drop the table

-- Add status column with default value
ALTER TABLE queries ADD COLUMN IF NOT EXISTS status VARCHAR DEFAULT 'pending';

-- Add timestamp columns
ALTER TABLE queries ADD COLUMN IF NOT EXISTS started_at TIMESTAMP;
ALTER TABLE queries ADD COLUMN IF NOT EXISTS completed_at TIMESTAMP;

-- Add error message column
ALTER TABLE queries ADD COLUMN IF NOT EXISTS error_message TEXT;

-- Update existing queries to have 'completed' status if they have a report
UPDATE queries 
SET status = 'completed' 
WHERE id IN (SELECT query_id FROM reports);

-- Verify the changes
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'queries'
ORDER BY ordinal_position;
