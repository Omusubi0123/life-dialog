from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.env_settings import env

engine = create_engine(env.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
