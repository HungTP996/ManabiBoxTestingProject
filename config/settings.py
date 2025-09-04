import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    BASE_URL = os.getenv("BASE_URL")
    ENVIRONMENT = os.getenv("ENVIRONMENT")
    PASSWORD = os.getenv("PASSWORD")

settings = Settings()
