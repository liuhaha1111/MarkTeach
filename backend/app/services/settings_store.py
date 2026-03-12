import json
import os
from datetime import datetime, timezone
from pathlib import Path

from app.security.crypto import encrypt_secret


class SettingsStore:
    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def from_env(cls) -> 'SettingsStore':
        configured = os.getenv('MARKTEACH_DATA_DIR')
        if configured:
            return cls(Path(configured))

        default_dir = Path(__file__).resolve().parents[2] / 'data'
        return cls(default_dir)

    @property
    def credentials_path(self) -> Path:
        return self.data_dir / 'credentials.enc.json'

    @property
    def workspace_path(self) -> Path:
        return self.data_dir / 'workspace.json'

    def save_credentials(self, provider: str, api_key: str, master_password: str) -> dict:
        current = self._read_json(self.credentials_path)
        encrypted = encrypt_secret(api_key, master_password)
        updated_at = datetime.now(timezone.utc).isoformat()

        current[provider] = {
            **encrypted,
            'updatedAt': updated_at,
        }
        self._write_json(self.credentials_path, current)

        return {
            'provider': provider,
            'maskedKey': self._mask_api_key(api_key),
            'updatedAt': updated_at,
        }

    def save_active_model(self, provider: str, model: str) -> dict:
        workspace = self._read_json(self.workspace_path)
        workspace['activeProvider'] = provider
        workspace['activeModel'] = model
        self._write_json(self.workspace_path, workspace)

        return {
            'activeProvider': provider,
            'activeModel': model,
        }

    def _read_json(self, path: Path) -> dict:
        if not path.exists():
            return {}
        return json.loads(path.read_text(encoding='utf-8'))

    def _write_json(self, path: Path, payload: dict) -> None:
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )

    def _mask_api_key(self, api_key: str) -> str:
        if len(api_key) <= 8:
            return '*' * len(api_key)
        return f"{api_key[:3]}{'*' * (len(api_key) - 7)}{api_key[-4:]}"
