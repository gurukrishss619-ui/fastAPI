from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.decl_api import declarative_base
from urllib.parse import quote_plus


PG_USER = "postgres"
PG_PASSWORD = quote_plus("@Guru619")
PG_HOST = "localhost"
PG_PORT = "5432"
PG_DATABASE = "fastapi_db"

BASE_URL = f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"

#Connection
engine = create_engine(BASE_URL)

#Session
sessionLocal = sessionmaker(expire_on_commit=False, autoflush=False, bind=engine)


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()
