from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Tax(Base):
    __tablename__ = "taxes"
    id = Column(Integer, primary_key=True)
    rate = Column(Integer)
    amount = Column(Integer)
