from configs.database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String


class Library(Base):
    __tablename__ = "library"

    __table_args__ = {"schema": "library"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    subtitle = Column(String)
    authors = Column(String)
    categories = Column(String)
    publication_date = Column(TIMESTAMP(timezone=False))
    editor = Column(String)
    description = Column(String)
    image = Column(String)
