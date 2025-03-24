import psycopg2
import os
import logging
from dotenv import load_dotenv

import psycopg2

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)  # Ensures logs are visible
logger = logging.getLogger(__name__)

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("PG_DATABASE"),
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
            host=os.getenv("PG_HOST"),
            port=os.getenv("PG_PORT")
        )
        logger.info("Successfully connected to PostgreSQL database!")  # Logging instead of print
        return conn
    except psycopg2.OperationalError as e:
        logger.error(f"❌ Database connection failed: {str(e)}")
        raise
