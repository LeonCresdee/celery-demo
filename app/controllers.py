from app.models import Job, Upload


class Jobs:
    def create_job():
        return Job(status="PENDING")


class Media:
    def create_media(name: str):
        return Upload(name=name)
