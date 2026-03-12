from app.security.crypto import decrypt_secret, encrypt_secret


def test_encrypt_roundtrip() -> None:
    payload = encrypt_secret('sk-123', 'master-pass')

    assert decrypt_secret(payload, 'master-pass') == 'sk-123'


def test_decrypt_fails_with_wrong_password() -> None:
    payload = encrypt_secret('sk-123', 'master-pass')

    try:
        decrypt_secret(payload, 'wrong-pass')
        assert False, 'expected decrypt to fail'
    except ValueError:
        assert True
