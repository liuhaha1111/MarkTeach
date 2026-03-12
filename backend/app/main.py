from fastapi import FastAPI

from app.api.export import router as export_router
from app.api.settings import router as settings_router
from app.api.transform import router as transform_router

app = FastAPI()


@app.get('/api/health')
def health() -> dict[str, bool]:
    return {'ok': True}


app.include_router(settings_router)
app.include_router(transform_router)
app.include_router(export_router)
