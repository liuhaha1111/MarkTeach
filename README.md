# MarkTeach Workbench (MVP)

## Run backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Run frontend

```bash
cd frontend
npm install
npm run dev
```

## Tests

```bash
cd backend
pytest -v

cd ../frontend
npm test
npm run e2e
```
