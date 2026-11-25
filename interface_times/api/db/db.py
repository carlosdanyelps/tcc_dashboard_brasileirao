import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

<<<<<<< HEAD

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://admin:123456@localhost:5433/dashboard_tcc"
)


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

=======
DATABASE_URL = (
    "postgresql://admin:123456@localhost:5433/dashboard_tcc"
)

engine = create_engine(DATABASE_URL)
>>>>>>> parent of 114037b (Merge branch 'main' of https://github.com/carlosdanyelps/tcc_dashboard_brasileirao)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()