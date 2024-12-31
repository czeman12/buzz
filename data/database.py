# data/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
import logging
from typing import Dict, Any


# Base class for declarative models
Base = declarative_base()


def initialize_database(engine):
    """
    Initialize the database by creating all tables.

    :param engine: SQLAlchemy engine instance.
    """
    from models.models import AggregateData, OptionData

    # Import all your models here
    Base.metadata.create_all(bind=engine)
    logging.info("Database tables created successfully.")
