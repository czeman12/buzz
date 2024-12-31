# models/__init__.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import yaml

# Load configuration
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

db_config = config["database"]["postgres"]

DATABASE_URL = (
    f"postgresql://{db_config['user']}:{db_config['password']}@"
    f"{db_config['host']}:{db_config['port']}/{db_config['name']}"
)

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base = declarative_base()

# Import all models here so that they are registered with SQLAlchemy
from .business import Business

# from .review import Review  # Example of importing additional models
