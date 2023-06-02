from datetime import date, datetime
from typing import List, Union

from pydantic import BaseModel, EmailStr, Field


class Address(BaseModel):
    addressee_name: Union[str, None] = Field()
    street: Union[str, None] = Field()
    street_number: Union[str, None] = Field()
    apartment: Union[str, None] = Field()
    city: Union[str, None] = Field()
    state: Union[str, None] = Field()
    postal_code: Union[str, None] = Field()
    country: Union[str, None] = Field()


class UserMasterSchema(BaseModel):
    """
    User schema for the User table
    """

    user_id: Union[str, None] = Field()
    user_type_id: Union[int, None] = Field()
    type_identification: Union[str, None] = Field()
    identity_document: Union[str, None] = Field()
    first_name: Union[str, None] = Field()
    last_name: Union[str, None] = Field()
    birthday_date: Union[date, None] = Field()
    country_phone_code_id: Union[int, None] = Field()
    phone_number: Union[int, None] = Field()
    email: Union[EmailStr, None] = Field()
    confirm_email: Union[bool, None] = False
    image_link: Union[str, None] = Field()
    address: List[Union[Address, None]] = Field(default=None)
    create_date: Union[datetime, None] = Field()


class UpdateUserMasterSchema(UserMasterSchema):
    id: Union[int, None] = Field()
    update_date: Union[datetime, None] = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


class ConfirmEmail(BaseModel):
    confirm_email: Union[bool, None] = True
