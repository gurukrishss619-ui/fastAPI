from databases.database import Base
from sqlalchemy import Column, Integer, VARCHAR

class BookTable(Base):
    __tablename__ = "Books"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(255))


