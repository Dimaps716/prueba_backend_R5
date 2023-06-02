from core.database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String


class RegisterModel(Base):
    """
    User model for the  table
    """

    __tablename__ = "users_register"

    __table_args__ = {"schema": "users_registration"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(25))
    last_name = Column(String(25))
    email = Column(String(80))
    password = Column(String())
    user_type_id = Column(Integer)
    create_date = Column(TIMESTAMP(timezone=False))
    load_date = Column(TIMESTAMP(timezone=False))
