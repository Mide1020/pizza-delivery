# import os
# from sqlalchemy import create_engine
# from sqlalchemy.orm import declarative_base, sessionmaker

# DATABASE_URL = os.getenv("DATABASE_URL")

# engine = create_engine(
#     DATABASE_URL,
#     connect_args={"sslmode": "require"},
#     pool_pre_ping=True
# )

# if not DATABASE_URL:
#     DATABASE_URL = "postgresql://postgres:1245@localhost/pizza_delivery"

# engine = create_engine(DATABASE_URL, echo=True)

# Base = declarative_base()
# Session = sessionmaker(bind=engine)



import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

# fallback for local development only
if not DATABASE_URL:
    DATABASE_URL = "postgresql://postgres:1245@localhost/pizza_delivery"

engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"},
    pool_pre_ping=True
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
