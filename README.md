# Submiq

NLP-based academic/professional submission verification platform. Final-year project.

## Structure

- `backend/` — FastAPI app (verification engine, NLP modules, API, DB models)
- `frontend/` — React app (applicant onboarding, results, admin dashboard)
- `data/` — synthetic dataset (raw → processed splits)
- `experiments/` — baseline, weight configs, evaluation scripts, results

## Build order

1. Repository + folders + `.gitignore`
2. Dataset inspection
3. Data preprocessing
4. Completeness baseline
5. Completeness module
6. Text-quality module
7. Consistency module
8. Llama plausibility module
9. GPTZero module
10. Scoring + gating
11. Automated evaluation
12. FastAPI
13. PostgreSQL
14. React applicant UI
15. Admin dashboard
16. Integration + final experiments

## Setup

```bash
cp .env.example .env
# fill in DATABASE_URL, GPTZERO_API_KEY, OLLAMA_HOST, SECRET_KEY

cd backend
pip install -r requirements.txt

cd ../frontend
npm install
```
