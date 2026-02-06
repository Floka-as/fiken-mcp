from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    fiken_api_key: str
    fiken_base_url: str = "https://api.fiken.no/api/v2"
    fiken_default_company_slug: str | None = None

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
