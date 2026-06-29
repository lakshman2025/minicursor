from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    LLM_ENDPOINT = os.getenv("LLM_ENDPOINT")
    LLM_API_KEY = os.getenv("LLM_API_KEY")
    LLM_MODEL = os.getenv("LLM_MODEL")
    