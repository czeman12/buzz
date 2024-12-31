# utils/db_utils.py

import psycopg2
from psycopg2 import pool
import logging
from typing import Optional, Any, Dict

# Initialize the connection pool as None
connection_pool: Optional[pool.SimpleConnectionPool] = None


def initialize_connection_pool(
    minconn: int = 1, maxconn: int = 10, db_config: Dict[str, Any] = {}
) -> None:
    """
    Initialize the PostgreSQL connection pool.

    :param minconn: Minimum number of connections in the pool.
    :param maxconn: Maximum number of connections in the pool.
    :param db_config: Database configuration dictionary.
    """
    global connection_pool
    try:
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            minconn,
            maxconn,
            user=db_config.get("user"),
            password=db_config.get("password"),
            host=db_config.get("host"),
            port=db_config.get("port"),
            database=db_config.get("database"),
        )
        if connection_pool:
            logging.info("Connection pool created successfully.")
    except psycopg2.Error as e:
        logging.critical(f"Error creating connection pool: {e}")
        raise


def get_db_connection() -> psycopg2.extensions.connection:
    """
    Acquire a connection from the pool.

    :return: A psycopg2 connection object.
    """
    global connection_pool
    if not connection_pool:
        logging.critical("Connection pool is not initialized.")
        raise Exception("Connection pool is not initialized.")
    try:
        conn = connection_pool.getconn()
        if conn:
            logging.debug("Acquired a connection from the pool.")
            return conn
    except psycopg2.Error as e:
        logging.error(f"Error acquiring connection: {e}")
        raise


def release_db_connection(conn: psycopg2.extensions.connection) -> None:
    """
    Release a connection back to the pool.

    :param conn: The psycopg2 connection object to release.
    """
    global connection_pool
    if connection_pool and conn:
        try:
            connection_pool.putconn(conn)
            logging.debug("Released the connection back to pool.")
        except psycopg2.Error as e:
            logging.error(f"Error releasing connection: {e}")
            raise


def close_all_connections() -> None:
    """
    Close all connections in the pool.
    """
    global connection_pool
    if connection_pool:
        connection_pool.closeall()
        logging.info("All connections in the pool have been closed.")
