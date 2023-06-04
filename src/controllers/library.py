from typing import Any

from fastapi import APIRouter, status

from schemas.library import LibraryRegistry, UpdateLibrary
from services import library

book_router = APIRouter(prefix="/library")


@book_router.get(
    "/{book}/searching",
    tags=["book"],
    status_code=status.HTTP_200_OK,
    summary="",
)
async def get_books_db(search_term: str):
    """
    Retrieve a user from the database using the specified user ID.

    Parameters:
    -----------
    user_id : str
        The ID of the user to retrieve.

    Returns:
    --------
    dict
        A dictionary containing the user information for the specified user ID.

    Raises:
    -------
    HTTPException
        If the user cannot be found or if there is an error retrieving the user.
    """
    return library.get_books_db(search_term)


@book_router.get(
    "/book",
    tags=["book"],
    status_code=status.HTTP_200_OK,
    summary="Retrieve users with the specified email address from the database",
)
async def single_books(
    id: int = None, authors: str = None, categories: str = None, title: str = None
) -> Any:
    """
    Retrieve users with the specified email address from the database.

    Parameters:
    -----------
    email : str
        The email address to search for.

    Returns:
    --------
    Any
        A list of dictionaries containing the user information for each user with the specified email address.

    Raises:
    -------
    HTTPException
        If there is an error retrieving the users.
    """
    return library.single_book(
        id=id, authors=authors, categories=categories, title=title
    )


# POST
@book_router.post(
    "/book/create/",
    tags=["book"],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user in the database using the specified form data.",
)
async def create_form(form_in: LibraryRegistry) -> dict:
    """
    Create a new user in the database using the specified form data.

    Parameters:
    -----------
    form_in : UserMasterSchema
        The data for the new user.

    Returns:
    --------
    dict
        A dictionary containing the user information for the newly created user.

    Raises:
    -------
    HTTPException
        If there is an error creating the user.
    """
    return library.create_book_library(form_in)


# PUT
@book_router.put(
    "/update/{book}",
    tags=["book"],
    status_code=status.HTTP_200_OK,
    summary="Update the user with the specified ID in the database using the specified form data.",
)
async def update_user(id: int, obj_updater: UpdateLibrary):
    """
    Update the user with the specified ID in the database using the specified form data.

    Parameters:
    -----------
    user_id : str
        The ID of the user to update.
    obj_updater : UpdateUserMasterSchema
        The data to update the user with.

    Returns:
    --------
    dict
        A dictionary containing the updated user information.

    Raises:
    -------
    HTTPException
        If there is an error updating the user.
    """
    return library.update_silgle_book(id, obj_updater)


# DELETE
@book_router.delete(
    "/delete/{book}",
    tags=["book"],
    status_code=status.HTTP_200_OK,
    summary="Delete the user with the specified ID from the database.",
)
def delete_user(id: int) -> dict:
    """
    Delete the user with the specified ID from the database.

    Parameters:
    -----------
    user_id : str
        The ID of the user to delete.

    Returns:
    --------
    dict
        A dictionary containing the deleted user information.

    Raises:
    -------
    HTTPException
        If there is an error deleting the user.
    """
    return library.delete_single_book(id)
