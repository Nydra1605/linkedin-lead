"""SQLAlchemy ORM & session helpers."""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, func
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

engine = create_engine(settings.database_url, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class Prospect(Base):
    __tablename__ = "prospects"

    id = Column(Integer, primary_key=True, index=True)
    linkedin_id = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String)
    title = Column(String)
    company = Column(String)
    state = Column(String, default="NEW")  # NEW / TOUCHED / REPLIED / QUALIFIED
    score = Column(Integer)
    metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# Create tables on first run
Base.metadata.create_all(bind=engine)