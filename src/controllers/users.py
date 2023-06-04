from typing import Any

from services import users_master
from fastapi import APIRouter, Depends, status
from schemas.users.users import UpdateUserMasterSchema, UserMasterSchema

user_router = APIRouter(prefix="/user/master")


@user_router.get(
    "/{user_id}",
    tags=["User_master"],
    status_code=status.HTTP_200_OK,
    summary="Retrieve a user from the database using the specified user ID",
)
async def get_user_by_id(user_id: str):
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
    return users_master.get_user_by_id(user_id)


@user_router.get(
    "/email/{email}",
    tags=["User_master"],
    status_code=status.HTTP_200_OK,
    summary="Retrieve users with the specified email address from the database",
)
async def get_users_by_email(email: str) -> Any:
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
    return users_master.get_users_by_email(email)


# POST
@user_router.post(
    "/create",
    tags=["User_master"],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user in the database using the specified form data.",
)
async def create_form(form_in: UserMasterSchema) -> dict:
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
    return users_master.create_user(form_in)


# PUT
@user_router.put(
    "/update/{user_id}",
    tags=["User_master"],
    status_code=status.HTTP_200_OK,
    summary="Update the user with the specified ID in the database using the specified form data.",
)
async def update_user(user_id: str, obj_updater: UpdateUserMasterSchema):
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
    return users_master.update_user(user_id, obj_updater)


# DELETE
@user_router.delete(
    "/delete/{user_id}",
    tags=["User_master"],
    status_code=status.HTTP_200_OK,
    summary="Delete the user with the specified ID from the database.",
)
def delete_user(user_id: str) -> dict:
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
    return users_master.delete_user_master(user_id)
