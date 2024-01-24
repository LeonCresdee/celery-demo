from app.extensions import db
from app.models import Media, Job
from worker import make_image
from flask import Blueprint, render_template, request
from flask import current_app as app
from werkzeug.utils import secure_filename
import os

root = Blueprint("root", __name__)


@root.get("/")
def index_page():
    return render_template("index.jinja2")


@root.get("/media")
def media_list_page():
    return render_template("media.jinja2")


@root.post("/media")
def upload_media():
    if "files" not in request.files:
        return {"error": "No file to upload."}, 400

    file = request.files["files"]

    if file.filename == "":
        return {"error": "No selected file."}, 400

    if file:
        filename = secure_filename(file.filename)
        media_dir = os.path.join(app.config["UPLOAD_FOLDER"], filename.split(".")[0])

        # Check directory doesn't already exist
        if os.path.isdir(media_dir):
            return {"error": "File already uploaded"}, 409

        # Create directory and save file
        os.mkdir(media_dir)
        file.save(os.path.join(media_dir, filename))

        db.session.add(Media(name=filename))

        # Create images
        make_image.delay("s", filename)
        make_image.delay("m", filename)
        make_image.delay("l", filename)

        db.session.commit()

    return {}, 200


@root.get("/media/<int:id>")
def media_page():
    return render_template("upload.jinja2")


@root.get("/jobs")
def jobs_page():
    return render_template("jobs.jinja2")
