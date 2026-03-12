from pydantic import BaseModel, Field


class EncryptedPayload(BaseModel):
    scheme: str = Field(default='aesgcm-pbkdf2-sha256-v1')
    iterations: int = Field(default=200_000, ge=100_000)
    salt: str
    nonce: str
    ciphertext: str
