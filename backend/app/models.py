from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import Integer,String
from .database import Base
class Product(Base):
    __tablename__="products"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    name:Mapped[str]=mapped_column(String(255))
    stock:Mapped[int]=mapped_column(Integer)
