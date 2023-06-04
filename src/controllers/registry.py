from fastapi import APIRouter, status

from schemas.users.user_register import UpdateRegistry, UserRegistry
from services import register

registry_router = APIRouter(prefix="/registry", tags=["Registry"])


@registry_router.get(
    "/all/{first_name}",
    status_code=status.HTTP_200_OK,
    summary="Retrieve registry data for the specified first name and user type",
)
def get_registry(first_name: str, user_type: int):
    """
    Retrieve registry data for the specified first name and user type.

    Parameters:
    -----------
    first_name : str
        The first name of the person for whom to retrieve registry data.
    user_type : int
        The type of user (e.g. admin, regular user) making the request for registry data.

    Returns:
    --------
    dict
        A dictionary containing the registry data for the specified first name and user type.

    Raises:
    -------
    HTTPException
        If the user is not authorized to access the registry data or if the registry data
        cannot be retrieved.
    """
    return register.get_registry(first_name=first_name, user_type=user_type)


@registry_router.get(
    "/{email}",
    status_code=status.HTTP_200_OK,
    summary="Retrieve a registry from the database using the specified email",
)
async def get_user_by_id(email: str):
    """
    Retrieve a registry from the database using the specified email.

    Parameters:
    -----------
    email : str
        The email of the registry to retrieve.

    Returns:
    --------
    dict
        A dictionary containing the registry information for the specified email.

    Raises:
    -------
    HTTPException
        If the registry cannot be found or if there is an error retrieving the registry.
    """
    return register.get_registry_by_email(email)


# POST
@registry_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new registry with the specified form data",
)
async def create_form(form_in: UserRegistry):
    """
    Create a new registry with the specified form data.

    Parameters:
    -----------
    form_in : UserRegistry
        The form data for the new registry.

    Returns:
    --------
    dict
        A dictionary containing the new registry data.

    Raises:
    -------
    HTTPException
        If the registry cannot be created or if there is an error sending the confirmation email.
    """
    data_register = register.create_registry(form_in)

    return data_register


# PUT
@registry_router.put(
    "/update/{email}",
    status_code=status.HTTP_200_OK,
    summary="Update a registry in the database using the specified email and update data",
)
async def update_user(email: str, obj_updater: UpdateRegistry):
    """
    Update a registry in the database using the specified email and update data.

    Parameters:
    -----------
    email : str
        The email of the registry to update.
    obj_updater : UpdateRegistry
        The data to update for the specified registry.

    Returns:
    --------
    dict
        A dictionary containing the updated registry data.

    Raises:
    -------
    HTTPException
        If the registry cannot be found or if there is an error updating the registry.
    """
    return register.updates_registry(email, obj_updater)
