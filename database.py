import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    
    DATABASE_URL = "postgresql+psycopg2://postgres:1234@127.0.0.1:5432/pizza_delivery"


connect_args = {"sslmode": "require"} if "render.com" in DATABASE_URL else {}


engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    echo=True,
)

print("Using DATABASE_URL:", DATABASE_URL)


Base = declarative_base()


Session = sessionmaker(bind=engine)
