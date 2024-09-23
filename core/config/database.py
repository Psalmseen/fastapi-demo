from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

POSTRGRES_PASSWD = "admin"
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{POSTRGRES_PASSWD}@localhost/postgres"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()