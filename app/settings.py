from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str
    echo_sql: bool = True
    test: bool = False
    project_name: str = "MatrixWorkflowHHAIHAIHIA"
    oauth_token_secret: str = "my_precious"
    log_level: str = "DEBUG"


settings = Settings()
