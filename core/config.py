import os
import pathlib

from dotenv import load_dotenv

env_file = os.environ.get("env_file", ".env")
load_dotenv(env_file)

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
PROJECT_NAME = os.getenv("PROJECT_NAME", "app")

app_id = os.getenv("app_id", None)
add_code = os.getenv("add_code", None)

