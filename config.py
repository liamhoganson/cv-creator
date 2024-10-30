import os
from dotenv import load_dotenv, find_dotenv

load_dotenv("env_vars.env")

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")

    @staticmethod
    def validate():
        if not Config.OPEN_AI_API_KEY:
            raise ValueError("OpenAI API key is required!")
        if not Config.SECRET_KEY:
            raise ValueError("Flask Secret Key is required!")

Config.validate()
