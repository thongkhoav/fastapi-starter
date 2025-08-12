from pydantic import BaseModel


class TokenPayload(BaseModel):
    sub: str  # Subject (email)
    exp: int  # Expiry timestamp
    user_id: int


class AccessTokenPayload(TokenPayload):
    full_name: str
    role: str


class RefreshTokenPayload(TokenPayload):
    jti: str  # Unique ID to revoke or identify the token
