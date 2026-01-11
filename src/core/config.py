import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, model_validator

# ---------------------------- Get env file ----------------------->

def get_env_file() -> str:
    env = os.getenv("ENVIRONMENT", "development")
    
    env_files = {
        "development": ".env.development",
        "production": ".env.production", 
    }
    
    env_file = env_files.get(env, ".env.development")
    
    if os.path.exists(env_file):
        return env_file
    else:
        return ".env"  
    
# ----------------------------- Settings -------------------------->

class Settings(BaseSettings):
    MONGO_URL: str = Field(default="mongodb://localhost:27017")
    DB_NAME: str = Field(default="learn_oidc")

    PUBLIC_KEY_PATH: str = Field(default="public.pem")
    PRIVATE_KEY_PATH: str = Field(default="private.pem")

    PRIVATE_KEY: str = ""
    PUBLIC_KEY: str = ""
    CSRF_KEY: str = Field(default="Anything you like")

    ALGORITHM: str = Field(default="RS256", description="JWT algorithm")
    ACCESS_TOKEN_TTL: int = Field(default=30, description="Access token TTL, unit = seconds")
    REFRESH_TOKEN_TTL: int = Field(default=7, description="Refresh token TTL, unit = days")

    CLIENT_ID: str = Field(default="Client ID", description="Google Client ID")
    CLIENT_SECRET: str = Field(default="Client Secret", description="Google Client Secret")

    @model_validator(mode="after")
    def load_keys_from_files(self):
        try:
            with open(self.PRIVATE_KEY_PATH, "r") as f:
                self.PRIVATE_KEY = f.read()
        except FileNotFoundError:
            raise ValueError(f"Private key not found at: {self.PRIVATE_KEY_PATH}")

        try:
            with open(self.PUBLIC_KEY_PATH, "r") as f:
                self.PUBLIC_KEY = f.read()
        except FileNotFoundError:
            raise ValueError(f"Public key not found at: {self.PUBLIC_KEY_PATH}")
        
        return self
    
    model_config = SettingsConfigDict(
        env_file=get_env_file(),
        env_file_encoding="utf-8",
        extra="ignore", 
    )

settings = Settings()