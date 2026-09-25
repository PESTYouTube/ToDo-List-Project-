from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.core.config import get_settings

settings = get_settings()
engine = create_engine(settings.database_url)
Sessionlocal = sessionmaker[Session](bind=engine)


def get_db():
    """Функция для инъекции сесии БД"""
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()
