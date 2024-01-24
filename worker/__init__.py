from celery import Celery
from config import Config
import os, subprocess


celery = Celery(__name__)
celery.config_from_object(Config.Worker)
celery.set_default()


SIZES = {
    "s": 320,
    "m": 500,
    "l": 1000,
}


@celery.task(name="make_image", ignore_result=False)
def make_image(size, filename):
    name, extension = filename.split(".", 1)

    input_path = os.path.join(celery.conf("UPLOAD_FOLDER"), name, filename)

    output_path = os.path.join(
        celery.conf.get("UPLOAD_FOLDER"),
        filename.split(".")[0],
        f"{name}_{size}.{extension}",
    )

    resolution = SIZES[size]
    cmd = ["ffmpeg", "-i", input_path, "-vf", f"scale={resolution}:-1", output_path]
    subprocess.run(cmd)
    return True
