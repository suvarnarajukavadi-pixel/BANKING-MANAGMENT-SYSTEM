import mysql.connector
from mysql.connector import Error
from config import Config
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db_tables(connection):
    """Execute bank_management.sql script if database tables do not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES LIKE 'admin'")
        if not cursor.fetchone():
            logger.info("Tables missing in database. Initializing database schema from bank_management.sql...")
            sql_path = os.path.join(Config.BASE_DIR, 'database', 'bank_management.sql')
            if os.path.exists(sql_path):
                with open(sql_path, 'r', encoding='utf-8') as f:
                    sql_statements = f.read()

                for statement in sql_statements.split(';'):
                    stmt = statement.strip()
                    if stmt:
                        try:
                            cursor.execute(stmt)
                        except Error as e:
                            # Ignore duplicate key / existing table warnings
                            pass
                logger.info("Database schema initialized successfully!")
        cursor.close()
    except Error as e:
        logger.error(f"Failed to initialize database tables: {e}")

def get_db_connection():
    """Establish and return a MySQL database connection with auto database setup."""
    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            port=Config.MYSQL_PORT,
            autocommit=True
        )
        init_db_tables(connection)
        return connection
    except Error as err:
        if getattr(err, 'errno', None) == 1049 or 'Unknown database' in str(err):
            logger.info(f"Database '{Config.MYSQL_DB}' not found. Auto-creating database...")
            try:
                conn_no_db = mysql.connector.connect(
                    host=Config.MYSQL_HOST,
                    user=Config.MYSQL_USER,
                    password=Config.MYSQL_PASSWORD,
                    port=Config.MYSQL_PORT,
                    autocommit=True
                )
                cursor = conn_no_db.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{Config.MYSQL_DB}`")
                cursor.close()
                conn_no_db.close()

                connection = mysql.connector.connect(
                    host=Config.MYSQL_HOST,
                    user=Config.MYSQL_USER,
                    password=Config.MYSQL_PASSWORD,
                    database=Config.MYSQL_DB,
                    port=Config.MYSQL_PORT,
                    autocommit=True
                )
                init_db_tables(connection)
                return connection
            except Error as init_err:
                logger.error(f"Auto database setup failed: {init_err}")
                return None
        else:
            logger.error(f"Error connecting to MySQL Database: {err}")
            return None

def fetch_one(query, params=None):
    """Execute a parameterized query and return a single row as a dictionary."""
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    except Error as err:
        logger.error(f"Database fetch_one error: {err} | Query: {query}")
        if conn and conn.is_connected():
            conn.close()
        return None

def fetch_all(query, params=None):
    """Execute a parameterized query and return all matching rows as dictionaries."""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except Error as err:
        logger.error(f"Database fetch_all error: {err} | Query: {query}")
        if conn and conn.is_connected():
            conn.close()
        return []

def execute_query(query, params=None, commit=True):
    """Execute a parameterized INSERT, UPDATE, or DELETE query."""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        if commit:
            conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return last_id if last_id else True
    except Error as err:
        logger.error(f"Database execute_query error: {err} | Query: {query}")
        if conn and conn.is_connected():
            conn.rollback()
            conn.close()
        return False
