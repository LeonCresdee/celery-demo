import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")

    class Worker:
        broker_url = os.getenv("CELERY_BROKER_URL")
        result_backend = os.getenv("CELERY_RESULT_BACKEND")
        task_ignore_result = True
