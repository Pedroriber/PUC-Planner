# Copilot Instructions

## Core Stack & Setup
- Django 5.2 + python-decouple; settings live in `hello_world/settings.py` and expect env vars like `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`.
- Use `cp .env.example .env` (or copy manually on Windows) before running; values are read through `config()`.
- Install deps with `pip install -r requirements.txt`; SQLite (`db.sqlite3`) is committed for convenience—backup lives in `db.sqlite3.backup`.
- Run `python manage.py migrate` then `python manage.py runserver`; `setup.py` automates install/migrate and reminds about superuser creation.
- When schema changes, run `python manage.py makemigrations appPUC_Planner` then `python manage.py migrate`; tests (when added) should run via `python manage.py test`.

## Architecture & Routing
- URL map is centralized in `hello_world/urls.py`; endpoints cover auth flows, disciplina CRUD under `/disciplinas`, and multiple fluxograma/grade screens.
- Views are expected under `hello_world/core` (typically `views.py`; create/update it if missing) and should render templates stored in `hello_world/templates`.
- Static assets live in `hello_world/static` (CSS hierarchy mirrors template names, JS in `js/`); Django serves them via `STATICFILES_DIRS`.
- Media uploads (if introduced) must respect `MEDIA_ROOT`/`MEDIA_URL`; URLs already append `static()` when `DEBUG` is true.
- Hot-reload during dev depends on `django_browser_reload` and the `__reload__/` route already included.

## Domain Models & Data
- Core domain lives in `appPUC_Planner/models.py`: `Curso` (degree, default 8 períodos), `Course` (code/name/credits/prereq CSV), and bridge `CursoDisciplina` (período + coluna `posicao`).
- Fluxograma layout relies on `CursoDisciplina.posicao` (1–8, validated) and optional `periodo`; keep new data within bounds so templates render correctly.
- `Course` prerequisites are stored as comma-separated codes; keep them consistent so UI/JS (e.g., `hello_world/static/js/buscaFluxograma.js`) can parse dependencies.
- `CourseForm` in `appPUC_Planner/forms.py` only exposes base fields; associating cursos happens through `CursoDisciplina` inlines or custom logic.
- Seed data is manual: use admin or CSV imports, and prefer `scripts/create_superuser.py` for quick auth bootstrapping.

## Auth & Sessions
- Custom auth model is `appPUC_Planner.CustomUser` (no username, login via `matricula`, required `email` + `nome_completo`); always reference it via `settings.AUTH_USER_MODEL`.
- Authentication stack uses `MatriculaBackend` plus Django's default backend; `LOGIN_URL`, `LOGIN_REDIRECT_URL`, and eager session expiry are configured in settings.
- Password validation only enforces min length 6; password reset emails print to console because `EMAIL_BACKEND` is `django.core.mail.backends.console.EmailBackend`.
- Quick dev superuser: run `python scripts/create_superuser.py` (creates matricula `admin`) or `python manage.py createsuperuser --matricula <id> --email <mail>`.
- `X_FRAME_OPTIONS` and Codespaces CSRF origins are already tweaked; keep changes compatible with GitHub preview embeds.

## Frontend & Templates
- Screen-specific templates live in `hello_world/templates` (e.g., `home.html`, `fluxograma*.html`, `grade_horaria.html`); shared pieces sit in `templates/includes/`.
- Course CRUD views use `hello_world/templates/courses/`; keep context variables (`form`, `object_list`, etc.) consistent to reuse the markup.
- CSS per page sits in `hello_world/static/css/*.css`; `global.css` + `main.css` define base tokens, so import them before page-specific styles.
- JS helpers such as `static/js/buscaFluxograma.js` and `grade_horaria.js` expect certain DOM IDs/classes; update both JS and template when renaming nodes.
- Images/assets under `hello_world/static/images` are referenced relatively; prefer optimized files there instead of inline data URIs.

## Admin & Tooling
- `appPUC_Planner/admin.py` wires `CustomUserAdmin`, `CourseAdmin`, and `CursoAdmin` with inline `CursoDisciplina` rows; reuse those inlines for anything touching the through model.
- `MAX_COLUMNS` is capped at 8 to match the fluxograma grid; adjust validators and templates together if you ever change the column count.
- Admin listings rely on `CourseAdmin.lista_cursos` to show placement; update it alongside any schema tweaks to `CursoDisciplina`.
- Browser reload middleware is enabled; run `python manage.py runserver` with `django_browser_reload` installed so hitting `__reload__/` keeps CSS/JS in sync.
- Sessions expire after 1 hour and `SESSION_SAVE_EVERY_REQUEST = True`; factor that into long-running AJAX or polling flows.
