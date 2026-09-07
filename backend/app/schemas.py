import re
from datetime import date, datetime

from app.models import ALLOWED_ENROLLMENT_STATUSES

# Practical email check for this assignment (not a full RFC parser)
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_student_data(data):
    """Validate and normalize student input for create/update.

    Returns:
        (normalized_dict, errors_dict)
        - On success: errors_dict is empty and normalized_dict has cleaned fields
        - On failure: normalized_dict is None and errors_dict maps field -> message

    Only reads mutable student fields — id / created_at / updated_at are ignored
    even if the client sends them.
    """
    if not isinstance(data, dict):
        return None, {"_schema": "Request body must be a JSON object"}

    errors = {}

    first_name = _require_non_empty_string(data, "first_name", errors)
    last_name = _require_non_empty_string(data, "last_name", errors)
    email = _validate_email(data, errors)
    date_of_birth = _validate_date_of_birth(data, errors)
    enrollment_status = _validate_enrollment_status(data, errors)

    if errors:
        return None, errors

    return {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "date_of_birth": date_of_birth,
        "enrollment_status": enrollment_status,
    }, {}


def serialize_student(student):
    """Convert a Student model instance into an API-ready dict."""
    return {
        "id": student.id,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "email": student.email,
        "date_of_birth": student.date_of_birth.isoformat(),
        "enrollment_status": student.enrollment_status,
        "created_at": _format_datetime(student.created_at),
        "updated_at": _format_datetime(student.updated_at),
    }


def _require_non_empty_string(data, field, errors):
    if field not in data or data[field] is None:
        errors[field] = f"{field} is required"
        return None

    value = data[field]
    if not isinstance(value, str):
        errors[field] = f"{field} must be a string"
        return None

    value = value.strip()
    if not value:
        errors[field] = f"{field} must not be empty"
        return None

    return value


def _validate_email(data, errors):
    if "email" not in data or data["email"] is None:
        errors["email"] = "email is required"
        return None

    value = data["email"]
    if not isinstance(value, str):
        errors["email"] = "email must be a string"
        return None

    value = value.strip().lower()
    if not value:
        errors["email"] = "email is required"
        return None

    if not _EMAIL_RE.match(value):
        errors["email"] = "email format is invalid"
        return None

    return value


def _validate_date_of_birth(data, errors):
    if "date_of_birth" not in data or data["date_of_birth"] is None:
        errors["date_of_birth"] = "date_of_birth is required"
        return None

    value = data["date_of_birth"]
    if not isinstance(value, str):
        errors["date_of_birth"] = "date_of_birth must be a string in YYYY-MM-DD format"
        return None

    try:
        dob = date.fromisoformat(value)
    except ValueError:
        errors["date_of_birth"] = "date_of_birth must be a valid date in YYYY-MM-DD format"
        return None

    if dob > date.today():
        errors["date_of_birth"] = "date_of_birth cannot be in the future"
        return None

    return dob


def _validate_enrollment_status(data, errors):
    if "enrollment_status" not in data or data["enrollment_status"] is None:
        errors["enrollment_status"] = "enrollment_status is required"
        return None

    value = data["enrollment_status"]
    if not isinstance(value, str):
        errors["enrollment_status"] = "enrollment_status must be a string"
        return None

    value = value.strip()
    if value not in ALLOWED_ENROLLMENT_STATUSES:
        allowed = ", ".join(ALLOWED_ENROLLMENT_STATUSES)
        errors["enrollment_status"] = (
            f"enrollment_status must be one of: {allowed}"
        )
        return None

    return value


def _format_datetime(value):
    """Format a datetime as ISO-8601 UTC (append Z for naive UTC values)."""
    if value is None:
        return None
    if isinstance(value, datetime) and value.tzinfo is None:
        return value.isoformat() + "Z"
    return value.isoformat()
