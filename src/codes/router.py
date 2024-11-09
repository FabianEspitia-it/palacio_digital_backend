from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from src.codes.schemas import *

from src.codes.crud import *


codes_router = APIRouter()


@codes_router.post("/disney/session_code/", tags=["disney_codes"])
def get_code_email(user_data: SessionCodes) -> JSONResponse:

    if user_data.password != os.getenv("PLATFORM_PASSWORD"):
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        code = get_code_email_by_email(email=user_data.email)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not code:
        raise HTTPException(status_code=404, detail="Code not found")

    return JSONResponse(content={
        "code": code,
    }, status_code=status.HTTP_200_OK)


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
