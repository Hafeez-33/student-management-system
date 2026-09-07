from pathlib import Path


# backend/ directory (parent of the app package)
BACKEND_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BACKEND_DIR / "students.db"


class Config:
    """Simple local-development configuration."""

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_PATH.as_posix()}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
