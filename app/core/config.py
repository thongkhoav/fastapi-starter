import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    ORACLE_USER: str = os.getenv("ORACLE_USER")
    ORACLE_PASSWORD: str = os.getenv("ORACLE_PASSWORD")
    ORACLE_HOST: str = os.getenv("ORACLE_HOST")
    ORACLE_PORT: str = os.getenv("ORACLE_PORT")
    ORACLE_SERVICE_NAME: str = os.getenv("ORACLE_SERVICE_NAME")
    
    @property
    def DATABASE_URL(self) -> str:
        return f"oracle+oracledb://{self.ORACLE_USER}:{self.ORACLE_PASSWORD}@{self.ORACLE_HOST}:{self.ORACLE_PORT}/?service_name={self.ORACLE_SERVICE_NAME}"
    
settings = Settings()