from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK, summary="Health Check")
def health_check():
    return JSONResponse(content={"status": "healthy"})
