from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import Config

engine = create_engine(Config.DATABASE_URI, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db_session = SessionLocal()
Base = declarative_base()


class DBCache:
    DIM_MOVE_CACHE = set()
    DIM_POKEMON_CACHE = set()
    DIM_STATS_CACHE = set()
