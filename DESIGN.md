# Design Note

## Data Model

A student is one SQLAlchemy model (`students` table) with an integer primary key `id`, required `first_name` and `last_name`, a unique indexed `email`, a SQL `DATE` for `date_of_birth`, and `enrollment_status` limited in application code to `active`, `graduated`, and `dropped`. `created_at` and `updated_at` are server-managed datetimes (`default` / `onupdate`). Clients cannot set `id` or timestamps through the validation helper; those fields are ignored if sent.

SQLite stores the file at `backend/students.db`. Tables are created with `db.create_all()` on app startup. That is enough for this assignment; there is no migration tool.

## API Design

The Flask app uses an application factory (`create_app`), shared extensions (`db`, `cors`), and a single `routes.py` module—no blueprints. Endpoints are `POST/GET /students`, `GET/PUT/DELETE /students/<id>`, plus `GET /health`.

List queries apply `enrollment_status` first, then count `total` and paginate with `page` / `per_page` (default 10, max 50), ordered by `id` ascending. The JSON envelope is `{ items, page, per_page, total, pages }`. Invalid page or status values return 400. An empty match is still 200 with `items: []`. CORS is enabled on the Flask app so the Vite origin can call the API locally without a reverse proxy.

Create and update run the same `validate_student_data` helper, then commit. Duplicate email is a unique-constraint `IntegrityError`, rolled back, and returned as 409—not 400 or 500. Missing ids are 404. PUT replaces all mutable fields so it stays aligned with full-body validation. Delete returns 200 with a short JSON message; a missing id is 404 so the UI can show “Student no longer exists.”


## Frontend Structure

`App.vue` is a thin shell. `StudentList.vue` owns list state (page, filter, loading, error) and toggles the form. After a successful delete it refetches the current filter; if the last row on a page was removed it steps back one page so the client does not request an empty trailing page. `StudentForm.vue` is one component for create and edit: client checks run first, then 400 `details` map onto fields and 409 sets a duplicate-email message. `StatusFilter.vue` and `Pagination.vue` only emit events; they do not call the API. `src/api/students.js` is the Axios client (`getStudents`, `getStudent`, `createStudent`, `updateStudent`, `deleteStudent`) using `VITE_API_BASE_URL`.


## Key Decisions

Flask + Flask-SQLAlchemy matches the preferred stack and keeps the surface small for a live walkthrough. SQLite avoids Docker and Postgres setup. Vue 3 is preferred by the company and is enough without Router or Pinia. An Axios module keeps HTTP out of templates. Pagination and filtering stay on the server so the UI cannot drift from the API contract.

## Trade-offs / Future Improvements

No auth, no search, and no frontend tests by choice of scope. PUT instead of PATCH is simpler to explain. Delete uses `window.confirm`. Next steps if needed: Postgres, Alembic, name search, and a few Vue tests around the form error mapping.
