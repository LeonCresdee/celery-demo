from app.extensions import db
from app.models import Job, Media
from billiard import current_process
from celery import shared_task
from config import Config
import os
import subprocess


SIZES = {
    "s": 320,
    "m": 500,
    "l": 1000,
}


@shared_task(name="make_image", ignore_result=False)
def make_image(size, media_id: int):
    # Create job entry
    media = db.session.execute(db.select(Media).get(media_id)).scalar_one_or_none()
    if not media:
        assert "Media mismangin"
        return False

    job = Job(
        status="STARTED",
        upload_id=media.id,
    )
    db.session.add(job)
    db.session.commit()

    try:
        # Build in/out paths for media
        name, extension = media.filename.split(".", 1)

        input_path = os.path.join(Config.UPLOAD_FOLDER, name, media.filename)

        output_path = os.path.join(
            Config.UPLOAD_FOLDER,
            media.filename.split(".")[0],
            f"{name}_{size}.{extension}",
        )

        # Generate image with FFMPEG
        resolution = SIZES[size]
        cmd = ["ffmpeg", "-i", input_path, "-vf", f"scale={resolution}:-1", output_path]
        subprocess.run(cmd)
    except:
        job.status = "FAILED"
        db.session.commit()
    else:
        job.status = "COMPLETED"
        job.completed_by = os.environ.get("HOSTNAME")
        db.session.commit()

    return True
