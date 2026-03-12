from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.settings_store import SettingsStore

router = APIRouter(prefix='/api/settings', tags=['settings'])


class CredentialsRequest(BaseModel):
    provider: Literal['openai', 'deepseek']
    apiKey: str = Field(min_length=1)
    masterPassword: str = Field(min_length=1)


class ActivateModelRequest(BaseModel):
    provider: Literal['openai', 'deepseek']
    model: str = Field(min_length=1)


@router.post('/credentials')
def save_credentials(payload: CredentialsRequest) -> dict:
    store = SettingsStore.from_env()
    result = store.save_credentials(
        provider=payload.provider,
        api_key=payload.apiKey,
        master_password=payload.masterPassword,
    )
    return {
        'ok': True,
        **result,
    }


@router.post('/activate-model')
def activate_model(payload: ActivateModelRequest) -> dict:
    store = SettingsStore.from_env()
    result = store.save_active_model(payload.provider, payload.model)
    return {
        'ok': True,
        **result,
    }
