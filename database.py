from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# MVP için SQLite veritabanı (proje klasöründe 'yonetim.db' oluşacak)
DATABASE_URL = "sqlite:///./yonetim.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tabloları oluştur (yoksa)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()