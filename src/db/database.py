from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

# ========================== Initialize Database ==========================
SQLALCHEMY_DATABASE_URL = "sqlite:///db.sqlite"
POSTGRES_DATABASE_URL = "postgresql://neondb_owner:npg_8iakdnomBwA7@ep-fragrant-unit-a1udg2zr-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
engine = create_engine(
    POSTGRES_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()