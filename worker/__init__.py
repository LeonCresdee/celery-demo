from flask import Flask
from celery import Celery, Task
from config import Config


# Application factory for celery
def init_celery(app: Flask) -> Celery:
    class ContextualTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery = Celery(app.name, task_cls=ContextualTask)
    celery.Task
    celery.config_from_object(Config.Worker)
    app.extensions["celery"] = celery
    return celery
