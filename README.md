# FitBuddy – AI Fitness Plan Generator

FitBuddy is a FastAPI + Jinja2 + SQLite web application based on the supplied project documentation. It generates a structured 7-day fitness plan, a nutrition/recovery tip, and an AI-updated plan from user feedback.

## Architecture

- Frontend: HTML + Jinja2 + CSS
- Backend: FastAPI
- AI: Google GenAI Python SDK
- Database: SQLite + SQLAlchemy
- Server: Uvicorn
- Testing: Pytest

## Important SDK update

The supplied documentation uses the older `google-generativeai` package and Gemini 1.5 model names. This implementation uses the current `google-genai` SDK and configurable current model names. Set `GEMINI_WORKOUT_MODEL` and `GEMINI_TIP_MODEL` in `.env` if your Google AI account exposes different models.

## Project structure

```text
FitBuddy/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── schemas.py
│   ├── routes.py
│   ├── gemini_generator.py
│   ├── gemini_flash_generator.py
│   └── updated_plan.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── result.html
│   ├── all_users.html
│   └── error.html
├── static/css/style.css
├── tests/test_app.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Windows + VS Code setup

1. Install Python 3.11 or newer.
2. Open this folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Create a virtual environment:

```powershell
python -m venv venv
```

5. Activate it:

```powershell
venv\Scripts\activate
```

6. Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

7. Create `.env` from `.env.example`.

PowerShell:

```powershell
Copy-Item .env.example .env
```

8. For a no-key local demo, leave `DEMO_MODE=true`. The UI and SQLite database will work with deterministic demo responses.

9. For real Gemini generation, put your Gemini API key in `.env`:

```text
GEMINI_API_KEY=your_real_key_here
DEMO_MODE=false
```

10. Start the server:

```powershell
uvicorn app.main:app --reload
```

11. Open:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/view-all-users

## Testing

With the virtual environment active:

```powershell
pytest -q
```

Expected result:

```text
3 passed
```

## Manual test

1. Open the home page.
2. Enter a name, unique User ID, age, weight, goal and intensity.
3. Click **Generate 7-Day Plan**.
4. Verify the result page shows the profile, 7-day plan and nutrition/recovery tip.
5. Enter feedback and click **Update Plan with AI**.
6. Open **Admin View** and verify both original and updated plans.
7. Check `/api/health` and `/docs`.

## API endpoints

- `GET /` – user form
- `POST /generate-workout` – generate and store a plan
- `POST /submit-feedback` – update latest plan from feedback
- `GET /view-all-users` – local admin dashboard
- `POST /delete-user/{user_id}` – delete a user and their plans
- `GET /api/health` – health check
- `GET /api/users` – JSON user summary
- `GET /docs` – FastAPI Swagger UI

## Safety

This application is a general wellness demo, not a medical diagnosis or treatment system. AI output should be reviewed before being used in real-world coaching. The prompts explicitly avoid extreme exercise, unsafe challenges, starvation/calorie restriction for minors, supplements/drugs, and medical claims.
