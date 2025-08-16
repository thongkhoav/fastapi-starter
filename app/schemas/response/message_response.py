from typing import Optional
from pydantic import BaseModel
from fastapi import status


class MessageResponse(BaseModel):
    message: str
    status_code: Optional[int] = status.HTTP_200_OK
