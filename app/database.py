from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

# <database system>://<user>:<password>@<ip address or host>/<database name>
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@' \
                          f'{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# the engine connects to the database system you are using
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# if running sqlalchemy on sqlite you have to also provide connect_args={'check_same_thread': False}
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# every model we define to create our tables will extend this base class
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
