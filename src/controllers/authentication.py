from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from utils.authentication import token_generator, very_token_email

authentication_router = APIRouter(prefix="/authentication", tags=["Authentication"])


@authentication_router.get("/verification/email")
async def email_verification(token: str):
    """Verifies a user's email token.

    HTTP GET endpoint that verifies a user's email token and returns the email address
    associated with the token if it's valid.

    Args:
        token (str): Email token to be verified.

    Returns:
        str: Email address associated with the token.

    Raises:
        HTTPException: If the token is invalid or has expired.
    """
    user = very_token_email(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user.RegisterModel.email


@authentication_router.post("/token")
async def generate_token(request_form: OAuth2PasswordRequestForm = Depends()):
    """Generates an authentication token.

    HTTP POST endpoint that generates an authentication token using the provided
    username and password.

    Args:
        request_form (OAuth2PasswordRequestForm): Form containing the username and
            password for authentication.

    Returns:
        dict: Dictionary containing the authentication token and token type.

    Raises:
        HTTPException: If the authentication credentials are invalid.
    """
    token = token_generator(request_form.username, request_form.password)
    return {"access_token": token, "token_type": "bearer"}


@authentication_router.get("/verification/token")
async def verification_token(token: str):
    """Verifies a user's email token.

    HTTP GET endpoint that verifies a user's email token and returns the email address
    associated with the token if it's valid.

    Args:
        token (str): Email token to be verified.

    Returns:
        str: Email address associated with the token.

    Raises:
        HTTPException: If the token is invalid or has expired.
    """
    user = very_token_email(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user.RegisterModel.email