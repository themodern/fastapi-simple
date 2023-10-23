from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create an SQLAlchemy engine and session
engine = create_engine("sqlite:///my_database.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the data model
class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    asset_name = Column(String)
    model_name = Column(String)
    market = Column(String)
    currency = Column(String)
