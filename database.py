import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings

Base = declarative_base()

import models

DSN = settings.database_url()
engine = sqlalchemy.create_engine(DSN)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
