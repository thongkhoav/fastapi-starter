# Auth URL paths mapping
from enum import Enum


class AuthPath(str, Enum):
    BASE = "/auth"
    ME = "/me"
    LOGIN = "/login"
    SIGNUP = "/signup"
    FORGOT_PASSWORD = "/forgot-password"
    RESET_PASSWORD = "/reset-password"
    REFRESH = "/refresh"
