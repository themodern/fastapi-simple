from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func 
from database import Base
# class Books(Base):
#     # define the table name
#     __tablename__ = "Books"

#     id = Column(Integer, primary_key=True, index=True)
#     asset_name = Column(String)
#     model_name = Column(String)
#     market = Column(String)
#     currency = Column(String)



class Research_Model(Base):
    __tablename__ = "Model"
    id = Column(Integer, primary_key=True, index=True)
    asset_name = Column(String)
    model_name = Column(String)
    market = Column(String)
    currency = Column(Integer)

class Portfolio(Base):
    __tablename__ = "Portfolio"
    id = Column(Integer, primary_key=True, index=True)
    asset_name = Column(String)
    create_time = Column(DateTime, default=func.now())     
    capital = Column(String)
    currency = Column(Integer)
    asset = Column(String)