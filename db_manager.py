import configparser
from sqlalchemy import create_engine


def get_database_config():
    # Initialize the configparser
    config = configparser.ConfigParser()

    # Read the config.ini file
    config.read("config.ini")

    # Extract the database configuration from the financials_psql section
    db_config = {
        "host": config.get("financials_psql", "host", fallback="localhost"),
        "port": config.getint("financials_psql", "port", fallback=5432),
        "dbname": config.get("financials_psql", "dbname", fallback="finance"),
        "user": config.get("financials_psql", "user", fallback="chris"),
        "password": config.get("financials_psql", "password", fallback="easyfast"),
    }
    return db_config


def get_engine():
    # Get database configuration
    db_config = get_database_config()
    
    # Create database engine using SQLAlchemy
    engine_url = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    engine = create_engine(engine_url)
    return engine
