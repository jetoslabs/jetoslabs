from pydantic import BaseSettings


class Settings(BaseSettings):
    # Logs
    LOG_SERIALIZE = False
    LOG_LEVEL = "DEBUG"
    ## App
    # FastApi
    NAME = "Jetoslabs app"
    DESCRIPTION = "Jetoslabs default app"
    VERSION = "0.1.0"
    CONTACT_NAME = "Jetoslabs"
    CONTACT_URL = "https://jetoslabs.com/contact/"
    CONTACT_EMAIL = "toanuragjha@gmail.com"
    # Uvicorn
    HOST = "localhost"
    PORT = 9999
    APP_RELOAD = True
    APP_WORKERS = 1
    API_V1_STR = "v1"
    # Configuration
    CONFIGURATION_PATH = ""
    CONFIGURATION_LOC = "../../../../jetoslabs-config-dev"
    # Tokeninzing
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"
