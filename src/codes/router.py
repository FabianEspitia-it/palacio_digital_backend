from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse

from src.codes.crud import *


codes_router = APIRouter()


@codes_router.post("/disney/session_code/", tags=["disney_codes"])
def get_code_email(user_email: str) -> JSONResponse:

    try:
        code = get_code_email_by_email(email=user_email)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not code:
        raise HTTPException(status_code=404, detail="Code not found")

    return JSONResponse(content={
        "code": code,
    }, status_code=status.HTTP_200_OK)


"""
@codes_router.patch("/disney/update_password", tags=["disney_codes"])
def update_password(info: ChangePasswordSchema) -> JSONResponse:
    
    Update the password associated with an email in the database.

    This function updates the password associated with the provided email in the database.

    Args:
        email (str): The email address to update the password for.
        password (str): The new password to associate with the email.
        db (Session, optional): Database session dependency. Defaults to a FastAPI 
                                dependency injection using `get_db()`.

    Returns:
        JSONResponse: A JSON response indicating the password was updated successfully.
    
    try:
        update_password_by_email(info=info)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return JSONResponse(content={
        "message": "Password updated successfully",
    }, status_code=status.HTTP_200_OK)
"""


@codes_router.get("/netflix/temporal_access/{email}", tags=["netflix_codes"])
def get_temporal_access(email: str) -> JSONResponse:

    try:

        link = get_temporal_access_code_by_email(email=email)

        if not link:
            raise HTTPException(status_code=404, detail="Link not found")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return JSONResponse(content={"link": link}, status_code=status.HTTP_200_OK)


@codes_router.get("/netflix/home_code/{email}", tags=["netflix_codes"])
def get_home_code(email: str) -> JSONResponse:

    try:
        link = get_home_code_by_email(email=email)

        if not link:
            raise HTTPException(status_code=404, detail="Link not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return JSONResponse(content={"link": link}, status_code=status.HTTP_200_OK)
