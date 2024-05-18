from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from db_manager import get_engine

engine = get_engine()
Base = declarative_base()
Session = sessionmaker(bind=engine)


# Context manager for managing sessions
@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class AggregateData(Base):
    __tablename__ = "aggregate_data"
    id = Column(Integer, primary_key=True)
    ticker = Column(String)
    date = Column(DateTime)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)


class OptionData(Base):
    __tablename__ = "option_data"
    id = Column(Integer, primary_key=True)
    ticker = Column(String)
    date = Column(DateTime)
    delta = Column(Float)
    gamma = Column(Float)
    theta = Column(Float)
    vega = Column(Float)
    rho = Column(Float)
