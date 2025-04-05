import os

import dotenv

dotenv.load_dotenv()


class Settings:
    TELEGRAM_BOTAPI_TOKEN = os.environ["TELEGRAM_BOTAPI_TOKEN"]
    TELEGRAM_ADMIN_IDS = os.environ["TELEGRAM_ADMIN_IDS"]

    COLLEGE_API_AUTH = os.environ["COLLEGE_API_AUTH"]

    MONGO_CONNECTION_STRING = os.environ["MONGO_CONNECTION_STRING"]
