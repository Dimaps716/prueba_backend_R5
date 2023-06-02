from sqlalchemy import (ARRAY, Boolean, Column, Integer, JSON, Numeric, String, TIMESTAMP, Text)

from configs.database import Base


class Users(Base):
    """
    user  model
    """

    __tablename__ = "users"

    __table_args__ = {"schema": "users"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(70), primary_key=True, index=True)
    user_type_id = Column(Integer)
    type_identification = Column(String(10))
    first_name = Column(String(150))
    last_name = Column(String(150))
    birthday_date = Column(TIMESTAMP(timezone=False), nullable=True, default=None)
    identity_document = Column(String(50))
    country_phone_code_id = Column(Integer)
    phone_number = Column(Numeric)
    email = Column(String(255))
    confirm_email = Column(Boolean, default=False)
    image_link = Column(Text())
    address = Column(ARRAY(JSON))
    update_date = Column(TIMESTAMP(timezone=False))
    create_date = Column(TIMESTAMP(timezone=False))
