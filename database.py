import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    DATABASE_URL = "postgresql://postgres:1234@127.0.0.1:5432/pizza_delivery"

   

    engine = create_engine(DATABASE_URL, echo=True)
else:
    
    engine = create_engine(
        DATABASE_URL,
        connect_args={"sslmode": "require"},
        pool_pre_ping=True,
        echo=True,
    )

Base = declarative_base()
Session = sessionmaker(bind=engine)
