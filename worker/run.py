from app import create_app
from celery import Celery
from flask import Flask


app: Flask = create_app()
app.app_context().push()

celery: Celery = app.extensions["celery"]
