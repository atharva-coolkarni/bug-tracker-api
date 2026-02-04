from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    JWT_ALGORITHM: str = "RS256"
    JWT_PRIVATE_KEY_PATH: str = "keys/jwt_private.pem"
    JWT_PUBLIC_KEY_PATH: str = "keys/jwt_public.pem"

    class Config:
        env_file = ".env"


settings = Settings()
