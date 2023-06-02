from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, EmailStr, Field


class LibraryBase(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = Field(
        ...,
    )
    subtitle: Optional[str] = None
    authors: Optional[str] = Field(
        ...,
    )
    categories: Optional[str] = Field(
        ...,
    )
    publication_date: Union[datetime, None] = Field(default=datetime.utcnow())
    editor: Optional[str] = Field(
        ...,
    )
    description: Optional[str] = None
    image: Optional[str] = None


class LibraryRegistry(LibraryBase):
    ...


class UpdateLibrary(LibraryBase):
    id: Union[int, None] = Field()
