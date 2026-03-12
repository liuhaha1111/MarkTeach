from fastapi import FastAPI

from app.api.settings import router as settings_router

app = FastAPI()


@app.get('/api/health')
def health() -> dict[str, bool]:
    return {'ok': True}


app.include_router(settings_router)
