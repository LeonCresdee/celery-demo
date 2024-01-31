from app.extensions import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from typing import List
from datetime import datetime


class Job(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str]
    started_on: Mapped[datetime] = mapped_column(server_default=func.now())
    changed_on: Mapped[datetime] = mapped_column(onupdate=func.now())
    completed_by: Mapped[str]
    upload_id: Mapped[int] = mapped_column(ForeignKey("media.id"))

    # Relationships
    media: Mapped["Media"] = relationship("Media", back_populates="jobs")


class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    uploaded_on: Mapped[datetime] = mapped_column(server_default=func.now())

    # Relationships
    jobs: Mapped[List[Job]] = relationship("Job", back_populates="media")

    def thumbnail(self, size: str = "s"):
        filename, extension = self.name.split(".", 1)

        return f"""
        <img src="/uploads/{filename}/{filename}_{size}.{extension}"></img>
        """
