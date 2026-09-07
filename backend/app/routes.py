import math

from flask import jsonify, request
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import ALLOWED_ENROLLMENT_STATUSES, Student
from app.schemas import serialize_student, validate_student_data


def register_routes(app):
    """Attach student CRUD routes to the Flask app."""

    @app.post("/students")
    def create_student():
        data = request.get_json(silent=True)
        if data is None:
            return _error(
                "Validation failed",
                {"_schema": "Request body must be a JSON object"},
                400,
            )

        normalized, errors = validate_student_data(data)
        if errors:
            return _error("Validation failed", errors, 400)

        student = Student(**normalized)
        db.session.add(student)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return _duplicate_email_error()

        return jsonify(serialize_student(student)), 201

    @app.get("/students")
    def list_students():
        page, per_page, pagination_errors = _parse_pagination()
        if pagination_errors:
            return _error("Validation failed", pagination_errors, 400)

        status_filter, status_errors = _parse_enrollment_status_filter()
        if status_errors:
            return _error("Validation failed", status_errors, 400)

        query = Student.query
        if status_filter is not None:
            query = query.filter_by(enrollment_status=status_filter)

        # Filter first, then count and paginate
        total = query.count()
        pages = math.ceil(total / per_page) if total > 0 else 0
        offset = (page - 1) * per_page

        students = (
            query.order_by(Student.id.asc()).offset(offset).limit(per_page).all()
        )

        return jsonify(
            {
                "items": [serialize_student(s) for s in students],
                "page": page,
                "per_page": per_page,
                "total": total,
                "pages": pages,
            }
        ), 200

    @app.get("/students/<int:student_id>")
    def get_student(student_id):
        student = db.session.get(Student, student_id)
        if student is None:
            return _not_found(student_id)
        return jsonify(serialize_student(student)), 200

    @app.put("/students/<int:student_id>")
    def update_student(student_id):
        student = db.session.get(Student, student_id)
        if student is None:
            return _not_found(student_id)

        data = request.get_json(silent=True)
        if data is None:
            return _error(
                "Validation failed",
                {"_schema": "Request body must be a JSON object"},
                400,
            )

        normalized, errors = validate_student_data(data)
        if errors:
            return _error("Validation failed", errors, 400)

        student.first_name = normalized["first_name"]
        student.last_name = normalized["last_name"]
        student.email = normalized["email"]
        student.date_of_birth = normalized["date_of_birth"]
        student.enrollment_status = normalized["enrollment_status"]

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return _duplicate_email_error()

        db.session.refresh(student)
        return jsonify(serialize_student(student)), 200

    @app.delete("/students/<int:student_id>")
    def delete_student(student_id):
        student = db.session.get(Student, student_id)
        if student is None:
            return _not_found(student_id)

        db.session.delete(student)
        db.session.commit()
        return jsonify(message=f"Student with id {student_id} deleted"), 200


def _parse_pagination():
    """Parse page/per_page query params. Returns (page, per_page, errors)."""
    errors = {}
    page = _parse_positive_int(request.args.get("page", "1"), "page", errors)
    per_page = _parse_positive_int(
        request.args.get("per_page", "10"), "per_page", errors, maximum=50
    )
    if errors:
        return None, None, errors
    return page, per_page, {}


def _parse_positive_int(raw_value, field, errors, maximum=None):
    try:
        value = int(raw_value)
    except (TypeError, ValueError):
        errors[field] = f"{field} must be a positive integer"
        return None

    if value < 1:
        errors[field] = f"{field} must be a positive integer"
        return None

    if maximum is not None and value > maximum:
        errors[field] = f"{field} must be at most {maximum}"
        return None

    return value


def _parse_enrollment_status_filter():
    """Parse optional enrollment_status query param."""
    raw = request.args.get("enrollment_status")
    if raw is None or raw == "":
        return None, {}

    value = raw.strip()
    if value not in ALLOWED_ENROLLMENT_STATUSES:
        allowed = ", ".join(ALLOWED_ENROLLMENT_STATUSES)
        return None, {
            "enrollment_status": f"enrollment_status must be one of: {allowed}"
        }
    return value, {}


def _error(error, details, status):
    return jsonify(error=error, details=details), status


def _not_found(student_id):
    return _error(
        "Not found",
        {"student": f"Student with id {student_id} not found"},
        404,
    )


def _duplicate_email_error():
    return _error(
        "Conflict",
        {"email": "A student with this email already exists"},
        409,
    )
