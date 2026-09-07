from datetime import date, timedelta


def _valid_student(**overrides):
    payload = {
        "first_name": "Ada",
        "last_name": "Lovelace",
        "email": "ada@example.com",
        "date_of_birth": "1815-12-10",
        "enrollment_status": "active",
    }
    payload.update(overrides)
    return payload


def test_create_student_success(client):
    response = client.post("/students", json=_valid_student())

    assert response.status_code == 201
    data = response.get_json()

    assert data["first_name"] == "Ada"
    assert data["last_name"] == "Lovelace"
    assert data["email"] == "ada@example.com"
    assert data["date_of_birth"] == "1815-12-10"
    assert data["enrollment_status"] == "active"
    assert isinstance(data["id"], int)
    assert data["id"] > 0
    assert data["created_at"]
    assert data["updated_at"]


def test_create_student_validation_failure(client):
    response = client.post(
        "/students",
        json=_valid_student(
            first_name="   ",
            email="not-an-email",
            date_of_birth=(date.today() + timedelta(days=1)).isoformat(),
            enrollment_status="pending",
        ),
    )

    assert response.status_code == 400
    body = response.get_json()
    assert body["error"] == "Validation failed"
    assert "details" in body
    assert "first_name" in body["details"]
    assert "email" in body["details"]
    assert "date_of_birth" in body["details"]
    assert "enrollment_status" in body["details"]


def test_get_student_not_found(client):
    response = client.get("/students/99999")

    assert response.status_code == 404
    body = response.get_json()
    assert body["error"] == "Not found"
    assert "student" in body["details"]


def test_create_student_duplicate_email(client):
    first = client.post("/students", json=_valid_student())
    assert first.status_code == 201

    # Same email, different casing — normalization still collides
    duplicate = client.post(
        "/students",
        json=_valid_student(
            first_name="Other",
            last_name="Person",
            email="ADA@example.com",
        ),
    )

    assert duplicate.status_code == 409
    body = duplicate.get_json()
    assert body["error"] == "Conflict"
    assert "email" in body["details"]

    # Session must remain usable after IntegrityError + rollback
    listing = client.get("/students")
    assert listing.status_code == 200
    assert listing.get_json()["total"] == 1


def test_list_students_filter_and_pagination(client):
    client.post(
        "/students",
        json=_valid_student(email="active1@example.com", enrollment_status="active"),
    )
    client.post(
        "/students",
        json=_valid_student(email="active2@example.com", enrollment_status="active"),
    )
    client.post(
        "/students",
        json=_valid_student(
            email="grad@example.com", enrollment_status="graduated"
        ),
    )

    filtered = client.get("/students?enrollment_status=active&page=1&per_page=1")
    assert filtered.status_code == 200
    body = filtered.get_json()

    assert body["total"] == 2
    assert body["pages"] == 2
    assert body["page"] == 1
    assert body["per_page"] == 1
    assert len(body["items"]) == 1
    assert body["items"][0]["enrollment_status"] == "active"


def test_update_student_success(client):
    created = client.post("/students", json=_valid_student())
    assert created.status_code == 201
    student = created.get_json()
    student_id = student["id"]
    original_updated_at = student["updated_at"]

    response = client.put(
        f"/students/{student_id}",
        json=_valid_student(
            first_name="Augusta",
            enrollment_status="graduated",
        ),
    )

    assert response.status_code == 200
    updated = response.get_json()
    assert updated["first_name"] == "Augusta"
    assert updated["enrollment_status"] == "graduated"
    assert updated["email"] == "ada@example.com"
    assert updated["updated_at"] != original_updated_at
