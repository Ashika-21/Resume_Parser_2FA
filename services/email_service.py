
import os
from email.message import EmailMessage

import aiosmtplib
from dotenv import load_dotenv

load_dotenv()


async def send_email_otp(recipient_email: str, otp: str) -> None:
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))

    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    sender_email = os.getenv("SENDER_EMAIL")

    if not smtp_username or not smtp_password or not sender_email:
        raise RuntimeError("Email SMTP settings are missing in .env")

    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Resume Parser - Email Verification OTP"

    message.set_content(
        f"""
Hello,

Your verification OTP is: {otp}

This OTP is valid for 5 minutes.

Please do not share this OTP with anyone.

Thank you,
Resume Parser Team
"""
    )

    await aiosmtplib.send(
        message,
        hostname=smtp_server,
        port=smtp_port,
        username=smtp_username,
        password=smtp_password,
        start_tls=True,
    )