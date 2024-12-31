# models/business.py

from sqlalchemy import Column, String, Integer, Float, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(Text, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    category = Column(String, nullable=True)
    rating = Column(Float, nullable=True)
    user_ratings_total = Column(Integer, nullable=True)
    place_id = Column(String, unique=True, nullable=False)
    types = Column(Text, nullable=True)  # JSON string or comma-separated types

    # Example relationship (if needed)
    # reviews = relationship("Review", back_populates="business")
