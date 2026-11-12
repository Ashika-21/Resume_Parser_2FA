
from datetime import datetime, timezone

from sqlalchemy import (
    String,
    Integer,
    Boolean,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class OTPChallenge(Base):
    __tablename__ = "otp_challenges"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    channel: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    otp_hash: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    totp_secret_encrypted: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    attempts: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )