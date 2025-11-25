"""
Quick database schema update script.
Run this to add the new status tracking columns to the queries table.
"""
from app.database import engine, Base
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_schema():
    """Add status tracking columns to queries table."""
    
    with engine.connect() as conn:
        try:
            # Check if status column exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='queries' AND column_name='status'
            """))
            
            if result.fetchone():
                logger.info("✅ Status column already exists!")
                return
            
            logger.info("Adding status tracking columns...")
            
            # Add new columns
            conn.execute(text("ALTER TABLE queries ADD COLUMN status VARCHAR DEFAULT 'pending'"))
            conn.execute(text("ALTER TABLE queries ADD COLUMN started_at TIMESTAMP"))
            conn.execute(text("ALTER TABLE queries ADD COLUMN completed_at TIMESTAMP"))
            conn.execute(text("ALTER TABLE queries ADD COLUMN error_message TEXT"))
            
            # Update existing queries
            conn.execute(text("""
                UPDATE queries 
                SET status = 'completed' 
                WHERE id IN (SELECT query_id FROM reports)
            """))
            
            conn.commit()
            
            logger.info("✅ Database schema updated successfully!")
            logger.info("New columns added: status, started_at, completed_at, error_message")
            
        except Exception as e:
            logger.error(f"❌ Failed to update schema: {e}")
            conn.rollback()
            raise

if __name__ == "__main__":
    update_schema()
