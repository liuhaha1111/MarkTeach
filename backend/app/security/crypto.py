import base64
import hashlib
import os

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from .models import EncryptedPayload


def _derive_key(password: str, salt: bytes, iterations: int) -> bytes:
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        iterations,
        dklen=32,
    )


def _b64_encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode('ascii')


def _b64_decode(value: str) -> bytes:
    return base64.urlsafe_b64decode(value.encode('ascii'))


def encrypt_secret(secret: str, password: str) -> dict:
    if not secret or not password:
        raise ValueError('secret and password are required')

    salt = os.urandom(16)
    nonce = os.urandom(12)
    iterations = 200_000
    key = _derive_key(password, salt, iterations)
    ciphertext = AESGCM(key).encrypt(nonce, secret.encode('utf-8'), None)

    payload = EncryptedPayload(
        iterations=iterations,
        salt=_b64_encode(salt),
        nonce=_b64_encode(nonce),
        ciphertext=_b64_encode(ciphertext),
    )
    return payload.model_dump()


def decrypt_secret(payload: dict, password: str) -> str:
    if not password:
        raise ValueError('password is required')

    encrypted = EncryptedPayload.model_validate(payload)
    salt = _b64_decode(encrypted.salt)
    nonce = _b64_decode(encrypted.nonce)
    ciphertext = _b64_decode(encrypted.ciphertext)
    key = _derive_key(password, salt, encrypted.iterations)

    try:
        plaintext = AESGCM(key).decrypt(nonce, ciphertext, None)
    except (InvalidTag, ValueError) as exc:
        raise ValueError('invalid password or payload') from exc

    return plaintext.decode('utf-8')
