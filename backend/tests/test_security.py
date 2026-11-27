import pytest

from app.core.errors import PermissionDeniedError
from app.core.security import (
    Role,
    create_access_token,
    decode_access_token,
    ensure_role,
    hash_password,
    verify_password,
)


def test_password_is_hashed_and_verifiable():
    hashed = hash_password("demo-password")

    assert hashed != "demo-password"
    assert verify_password("demo-password", hashed)
    assert not verify_password("otra-password", hashed)


def test_access_token_carries_tenant_and_role():
    token = create_access_token(subject="user-1", tenant_id="tenant-a", role=Role.AGENT)
    payload = decode_access_token(token)

    assert payload["sub"] == "user-1"
    assert payload["tenant_id"] == "tenant-a"
    assert payload["role"] == "agent"


def test_tampered_token_is_rejected():
    token = create_access_token(subject="user-1", tenant_id="tenant-a", role=Role.OWNER)
    tampered = token[:-2] + ("aa" if not token.endswith("aa") else "bb")

    with pytest.raises(PermissionDeniedError):
        decode_access_token(tampered)


def test_role_check_allows_and_denies():
    ensure_role("admin", {Role.OWNER, Role.ADMIN})

    with pytest.raises(PermissionDeniedError):
        ensure_role("analyst", {Role.OWNER, Role.ADMIN})
