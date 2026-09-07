from datetime import datetime, timezone

from app.extensions import db

# Single source of truth for allowed status values (reused by validation / API)
ALLOWED_ENROLLMENT_STATUSES = ("active", "graduated", "dropped")


def _utc_now():
    """Naive UTC timestamp — SQLite stores datetimes without timezone info."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    date_of_birth = db.Column(db.Date, nullable=False)
    enrollment_status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=_utc_now)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=_utc_now, onupdate=_utc_now
    )

    def __repr__(self):
        return f"<Student {self.id} {self.email}>"
