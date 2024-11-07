from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse

from src.codes.crud import *


codes_router = APIRouter()


@codes_router.get("/disney/session_code/{email}", tags=["disney_codes"])
def get_code_email(email: str) -> JSONResponse:

    try:
        code = get_code_email_by_email(email=email)
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
