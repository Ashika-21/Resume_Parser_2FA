
import secrets
from datetime import datetime, timedelta, timezone

from services.password_service import (
    hash_password,
    verify_password
)


def generate_otp() -> str:
    return str(secrets.randbelow(900000) + 100000)


def hash_otp(otp: str) -> str:
    return hash_password(otp)


def verify_otp(
    entered_otp: str,
    stored_hash: str
) -> bool:
    return verify_password(
        entered_otp,
        stored_hash
    )


def get_otp_expiry() -> datetime:
    return datetime.now(timezone.utc) + timedelta(minutes=5)