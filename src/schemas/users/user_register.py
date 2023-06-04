from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = Field(
        ...,
    )
    password: Optional[str] = Field(
        ...,
    )
    load_date: Union[datetime, None] = Field(default=datetime.utcnow())
    create_date: Union[datetime, None] = Field(default=datetime.utcnow())


class UserRegistry(UserBase):
    ...


class UpdateRegistry(UserBase):
    id: Union[int, None] = Field()
