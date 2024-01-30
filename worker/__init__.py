from . import tasks
from celery import Celery
from config import Config

celery = Celery(__name__)
celery.config_from_object(Config.Worker)
celery.set_default()
