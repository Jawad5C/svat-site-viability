# SVAT Backend

API for the Site Viability Assessment Tool. FastAPI app with versioned routes under `/api/v1`.

## Run locally

From the **project root** (the folder that contains `backend/`), run:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

On Windows: `.venv\Scripts\activate` instead of `source .venv/bin/activate`.

**Note:** On macOS, use `python3` (not `python`). If the venv is already created, you only need `source .venv/bin/activate` then `uvicorn ...`.

- **API:** http://localhost:8000  
- **Swagger UI:** http://localhost:8000/docs  
- **ReDoc:** http://localhost:8000/redoc  
- **Health:** http://localhost:8000/health  

## Main endpoint

- **POST /api/v1/assessments** — Run a site viability assessment.

  Body:
  - `assessment_type`: `"full"` | `"post_fid"` | `"post_construction"`
  - `location`: `{ "latitude": number, "longitude": number }` (US only for MVP)

  Returns metrics relevant to the chosen type (stub values until data sources are wired in).
