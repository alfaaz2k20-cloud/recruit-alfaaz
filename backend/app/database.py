from sqlmodel import SQLModel, create_engine, Session
from app.config import settings

connect_args = {}
# Aiven requires SSL. psycopg2 handles this via sslmode=require.
# We will only use this if it's a postgresql URL that doesn't already have sslmode in it.
if "postgres" in settings.database_url and "sslmode=" not in settings.database_url:
    connect_args["sslmode"] = "require"

engine = create_engine(
    settings.database_url,
    echo=False,
    pool_pre_ping=True,
    connect_args=connect_args,
)


def init_db():
    # Import all models so SQLModel sees them before creating tables
    # from app import models  # noqa: F401
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
