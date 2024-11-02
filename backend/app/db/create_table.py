from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.db_model import Base


DATABASE_URL = "postgresql://user:password@postgres:5432/db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
