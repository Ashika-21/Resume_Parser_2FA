
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.user import User
from models.otp import OTPChallenge
from schemas.auth import RegisterRequest

from services.password_service import hash_password, verify_password
from services.otp_service import (
    generate_otp,
    hash_otp,
    verify_otp,
    get_otp_expiry
)
from services.token_service import create_access_token
from services.email_service import send_email_otp


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


class LoginRequest(BaseModel):
    email: str
    password: str = Field(min_length=8)


class VerifyOTPRequest(BaseModel):
    user_id: int
    channel: str = "email"
    otp: str = Field(min_length=6, max_length=6)


@router.post("/register")
async def register_user(
    user_data: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(
            select(User).where(User.email == user_data.email)
        )

        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="Email already registered"
            )

        new_user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            phone=user_data.phone,
            password_hash=hash_password(user_data.password),
            is_active=False
        )

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return {
            "message": "Registration successful. Please complete email OTP verification.",
            "user_id": new_user.id,
            "full_name": new_user.full_name,
            "email": new_user.email,
            "is_active": new_user.is_active
        }

    except HTTPException:
        raise
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Registration failed"
        )


@router.post("/login")
async def login_user(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.email == login_data.email)
    )

    user = result.scalar_one_or_none()

    if not user or not verify_password(
        login_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Please complete email OTP verification first"
        )

    access_token = create_access_token(user.id)

    return {
        "message": "Login successful",
        "user_id": user.id,
        "is_active": user.is_active,
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/request-otp/{user_id}")
async def request_otp(
    user_id: int,
    channel: str = "email",
    db: AsyncSession = Depends(get_db)
):
    try:
        if channel != "email":
            raise HTTPException(
                status_code=400,
                detail="Only email OTP is supported"
            )

        result = await db.execute(
            select(User).where(User.id == user_id)
        )

        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        if user.is_active:
            raise HTTPException(
                status_code=400,
                detail="User is already active"
            )

        otp = generate_otp()

        challenge = OTPChallenge(
            user_id=user.id,
            channel="email",
            otp_hash=hash_otp(otp),
            expires_at=get_otp_expiry(),
            attempts=0,
            is_verified=False
        )

        db.add(challenge)
        await db.flush()

        try:
            await send_email_otp(user.email, otp)

        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=502,
                detail="Email OTP delivery failed. Check your SMTP configuration and recipient email."
            )

        await db.commit()
        await db.refresh(challenge)

        return {
            "message": "OTP sent successfully through email",
            "challenge_id": challenge.id,
            "user_id": user.id,
            "channel": "email",
            "expires_in_minutes": 5
        }

    except HTTPException:
        raise
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to generate OTP"
        )


@router.post("/verify-2fa")
async def verify_2fa(
    verification: VerifyOTPRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        if verification.channel != "email":
            raise HTTPException(
                status_code=400,
                detail="Only email OTP verification is supported"
            )

        result = await db.execute(
            select(User).where(User.id == verification.user_id)
        )

        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        result = await db.execute(
            select(OTPChallenge)
            .where(
                OTPChallenge.user_id == user.id,
                OTPChallenge.channel == "email",
                OTPChallenge.is_verified.is_(False)
            )
            .order_by(OTPChallenge.id.desc())
            .limit(1)
        )

        challenge = result.scalar_one_or_none()

        if not challenge:
            raise HTTPException(
                status_code=404,
                detail="No pending email OTP challenge found"
            )

        if challenge.expires_at <= datetime.now(timezone.utc):
            raise HTTPException(
                status_code=400,
                detail="OTP has expired. Request a new OTP."
            )

        if challenge.attempts >= 5:
            raise HTTPException(
                status_code=429,
                detail="Maximum OTP attempts exceeded"
            )

        challenge.attempts += 1

        if not verify_otp(
            verification.otp,
            challenge.otp_hash
        ):
            await db.commit()
            raise HTTPException(
                status_code=400,
                detail="Invalid OTP"
            )

        challenge.is_verified = True
        user.is_active = True

        access_token = create_access_token(user.id)

        await db.commit()

        return {
            "message": "Email OTP verification successful",
            "user_id": user.id,
            "is_active": user.is_active,
            "access_token": access_token,
            "token_type": "bearer"
        }

    except HTTPException:
        raise
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="OTP verification failed"
        )