from celery import shared_task
import subprocess
import os
from config import Config

SIZES = {
    "s": 320,
    "m": 500,
    "l": 1000,
}


@shared_task(name="make_image", ignore_result=False)
def make_image(size, filename):
    name, extension = filename.split(".", 1)

    input_path = os.path.join(Config.UPLOAD_FOLDER, name, filename)

    output_path = os.path.join(
        Config.UPLOAD_FOLDER,
        filename.split(".")[0],
        f"{name}_{size}.{extension}",
    )

    resolution = SIZES[size]
    cmd = ["ffmpeg", "-i", input_path, "-vf", f"scale={resolution}:-1", output_path]
    subprocess.run(cmd)
    return True
