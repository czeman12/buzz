# factories/session_factory.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.config_manager import get_financial_db_config
from sqlalchemy.ext.declarative import declarative_base
import logging

Base = declarative_base()


def create_session_factory():
    """Create both engine and session factory."""
    db_config = get_financial_db_config()  # Load the DB config
    DATABASE_URI = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

    # Create the engine
    engine = create_engine(DATABASE_URI, echo=True, pool_pre_ping=True)

    # Create the session factory
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Initialize the database (creating tables)
    initialize_database(engine)

    return SessionLocal  # This is a sessionmaker


def initialize_database(engine):
    """Initialize the database by creating all tables."""
    from models.models import AggregateData, OptionData  # Import all your models here

    Base.metadata.create_all(bind=engine)  # This will create the tables in the database
    logging.info("Database tables created successfully.")
