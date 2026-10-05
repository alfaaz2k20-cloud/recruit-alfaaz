# Alfaaz Recruit

A browser-based volunteer assessment for Alfaaz Collective. Combines a
7-scenario Situational Judgment Test (SJT) with 14 short behavioral
games. Reports two independent evidence streams to a human recruiter.

**Status:** Calibration beta. Not validated. Not a selection decision.
See `docs/` for research foundation and validation roadmap.

## Structure

- `frontend/` — React + Vite candidate app
- `backend/` — FastAPI + SQLModel scoring and telemetry
- `config/` — SJT items, task definitions, feature schemas
- `docs/` — research foundation, build spec, validation plan

## Local development

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000