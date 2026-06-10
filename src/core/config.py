import functools
from datetime import timedelta, timezone
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    root_dir: Path = Path(__file__).resolve().parent.parent.parent
    src_dir: Path = root_dir.joinpath("src")
    env_file: Path = src_dir.joinpath(".env.local")

    PROJECT_NAME: str = "rate-watch"

    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 5000
    SERVER_WORKERS_COUNT: int = 5

    HTTP_TIMEOUT: int = 15

    CBR_URL: str = "https://www.cbr.ru/currency_base/daily/"

    MAIN_DEPLOYMENT_NAME: str = "main-deployment"
    MAIN_FLOW_NAME: str = "main-flow"
    MAIN_FLOW_INTERVAL_IN_SEC: int = 300

    ENVIRONMENT: str = "local"
    TIME_ZONE: timezone = timezone(offset=timedelta(hours=+3))
    CORS_ALLOW_ORIGIN_LIST: str = "*"

    USE_CORS_MIDDLEWARE: bool = True
    USE_TIMER_MIDDLEWARE: bool = False

    POSTGRES_HOST: str = "rate-watch-db"
    POSTGRES_PORT: int = 5532
    POSTGRES_USER: str = "rate-watch-db"
    POSTGRES_PASSWORD: str = "rate-watch-db"
    POSTGRES_DB: str = "rate-watch-db"

    MINIO_HOST: str = "rate-watch-s3"
    MINIO_PORT: int = 9500
    MINIO_WEB_PORT: int = 9510
    MINIO_ROOT_USER: str = "rate-watch-s3"
    MINIO_ROOT_PASSWORD: str = "rate-watch-s3"
    MINIO_ACCESS_KEY_ID: str = "rate-watch-s3"
    MINIO_SECRET_ACCESS_KEY: str = "rate-watch-s3"
    MINIO_REGION_NAME: str = "eu-central-1"
    MINIO_DEFAULT_BUCKET: str = "rate-watch-bucket"

    REDIS_HOST: str = "rate-watch-redis"
    REDIS_PORT: int = 6579
    REDIS_PASSWORD: str = "rate-watch-redis"
    REDIS_DB: int = 0

    PREFECT_PORT: int = 4500
    PREFECT_SERVER_API_HOST: str = "0.0.0.0"
    PREFECT_API_URL: str = f"http://{PREFECT_SERVER_API_HOST}:{PREFECT_PORT}/api"


    @functools.cached_property
    def cors_allow_origins(self) -> list[str]:
        return self.CORS_ALLOW_ORIGIN_LIST.split("&")

    @functools.cached_property
    def postgres_dsn(self) -> str:
        postgres_host = "localhost" if self.ENVIRONMENT == "local" else self.POSTGRES_HOST
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{postgres_host}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @functools.cached_property
    def s3_dsn(self) -> str:
        s3_host = "localhost" if self.ENVIRONMENT == "local" else self.MINIO_HOST
        return f"http://{s3_host}:{self.MINIO_PORT}"

    model_config = SettingsConfigDict(
        env_file=env_file if env_file else None,
        env_file_encoding="utf-8",
        extra="allow",
    )


@functools.lru_cache()
def settings() -> Settings:
    return Settings()
