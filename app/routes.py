from app.extensions import db
from app.models import Media, Job
from worker import tasks
from flask import Blueprint, render_template, request, send_file, abort
from flask import current_app as app
from werkzeug.utils import secure_filename
import os

root = Blueprint("root", __name__)


@root.get("/")
def index_page():
    """
    Homepage and page to upload images.
    """

    return render_template("index.jinja2")


@root.get("/media")
def media_list_page():
    """
    Page listing uploaded media
    """

    media = db.session.execute(db.select(Media)).scalars()

    return render_template("media.jinja2", media=media)


@root.post("/media")
def upload_media():
    """
    Endpoint to upload media files.

    TODO: Check filetype is compatible.
    """

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

        # Create media entry
        media = Media(name=filename)
        db.session.add(media)

        # Create images
        tasks.make_image.delay("s", media.id)
        tasks.make_image.delay("m", media.id)
        tasks.make_image.delay("l", media.id)

        db.session.commit()

    return {}, 200


@root.get("/media/<int:id>")
def media_page():
    """
    Page to view individual images.
    """
    return render_template("upload.jinja2")


@root.get("/uploads/<path:path>")
def media_uploads(path):
    path = path.split("/")
    path = os.path.join(app.config.get("UPLOAD_FOLDER"), *path)

    if os.path.isfile(path):
        return send_file(path)
    else:
        abort(404)


@root.get("/jobs")
def jobs_list_page():
    """
    Page listing jobs
    """

    jobs = db.session.execute(db.select(Job)).scalars()
    return render_template("jobs.jinja2", jobs=jobs)
