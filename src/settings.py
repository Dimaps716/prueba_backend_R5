import os

from dotenv import load_dotenv

load_dotenv()


# > This class is used to store all the environment variables that are used in the application
class Settings:
    BASE_API_PREFIX = "/api"
    MACHINE = os.getenv("MACHINE")

    # email
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_FROM = os.getenv("MAIL_FROM")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_TLS = os.getenv("MAIL_TLS")
    MAIL_SSL = os.getenv("MAIL_SSL")
    USE_CREDENTIALS = os.getenv("USE_CREDENTIALS")
    VALIDATE_CERTS = os.getenv("VALIDATE_CERTS")
    SECRET = os.getenv("SECRET")
    SITE_URL = os.getenv("SITE_URL")
    SITE_NAME = os.getenv("SITE_NAME")

    if MACHINE == "GCP":
        ROOT_PATH = BASE_API_PREFIX
    else:
        ROOT_PATH = ""
