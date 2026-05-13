from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_OP_USER: str = "test_user"
    DB_OP_PASSWORD: str = "test_password"
    DB_OP_HOST: str = "localhost"
    DB_OP_PORT: int = 5432
    DB_OP_NAME: str = "test_db"

    DB_ADMIN_USER: str = "test_admin_user"
    DB_ADMIN_PASSWORD: str = "test_admin_password"
    DB_ADMIN_HOST: str = "localhost"
    DB_ADMIN_PORT: int = 5432
    DB_ADMIN_NAME: str = "test_admin_db"

    JWT_EXPIRES_MINUTES: int = 60
    JWT_SECRET: str = "test_secret"
    JWT_ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(
        env_file=("develop.env", ".env", ".env.example"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()