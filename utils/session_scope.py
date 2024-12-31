# utils/session_scope.py

from contextlib import contextmanager
from sqlalchemy.orm import Session
import logging
from typing import Generator


@contextmanager
def session_scope(session_factory) -> Generator[Session, None, None]:
    """Provide a transactional scope around a series of operations."""
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logging.error(f"Session rollback due to exception: {e}")
        raise
    finally:
        session.close()
