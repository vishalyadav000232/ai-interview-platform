import logging
import resend

from app.core.config import settings
from app.services.interface.email_service import EmailServiceInterface

logger = logging.getLogger(__name__)


class EmailService(EmailServiceInterface):
    def __init__(self):
        resend.api_key = settings.RESEND_API_KEY

    async def send_email_verification(
        self,
        email: str,
        verification_link: str
    ) -> None:
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <body style="margin:0;padding:0;background:#f4f7fb;font-family:Arial,sans-serif;">
            <div style="max-width:600px;margin:40px auto;background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.08);">
                
                <div style="background:linear-gradient(135deg,#4f46e5,#7c3aed);padding:32px;text-align:center;color:white;">
                    <h1 style="margin:0;font-size:28px;">AI Interview Platform</h1>
                    <p style="margin:10px 0 0;font-size:15px;">Prepare smarter. Interview better.</p>
                </div>

                <div style="padding:32px;color:#111827;">
                    <h2 style="margin-top:0;font-size:24px;">Verify your email</h2>

                    <p style="font-size:16px;line-height:1.6;color:#4b5563;">
                        Welcome! Please confirm your email address to activate your account and start using AI-powered interview preparation.
                    </p>

                    <div style="text-align:center;margin:32px 0;">
                        <a href="{verification_link}"
                           style="background:#4f46e5;color:#ffffff;text-decoration:none;padding:14px 28px;border-radius:10px;font-size:16px;font-weight:bold;display:inline-block;">
                            Verify Email
                        </a>
                    </div>

                    <p style="font-size:14px;line-height:1.6;color:#6b7280;">
                        This link will expire in <strong>24 hours</strong>. If you did not create this account, you can safely ignore this email.
                    </p>

                    <hr style="border:none;border-top:1px solid #e5e7eb;margin:28px 0;">

                    <p style="font-size:12px;color:#9ca3af;word-break:break-all;">
                        If the button does not work, copy and paste this link into your browser:<br>
                        {verification_link}
                    </p>
                </div>

                <div style="background:#f9fafb;padding:18px;text-align:center;font-size:12px;color:#9ca3af;">
                    © 2026 AI Interview Platform. All rights reserved.
                </div>
            </div>
        </body>
        </html>
        """

        params = {
            "from": settings.EMAIL_FROM,
            "to": [email],
            "subject": "Verify your email - AI Interview Platform",
            "html": html_content,
        }

        try:
            resend.Emails.send(params)

            logger.info(
                "Verification email sent successfully",
                extra={"email": email}
            )

        except Exception:
            logger.exception(
                "Failed to send verification email",
                extra={"email": email}
            )
    
    async def send_password_reset_email(
    self,
    email: str,
    reset_link: str
) -> None:

        params = {
            "from": settings.EMAIL_FROM,
            "to": [email],
            "subject": "Reset your password",
            "html": f"""
                <h2>Reset Your Password</h2>
                <p>Click the link below to reset your password:</p>
                <a href="{reset_link}">Reset Password</a>
                <p>This link will expire in 15 minutes.</p>
                <p>If you did not request this, please ignore this email.</p>
            """,
        }

        try:
            resend.Emails.send(params)

            logger.info(
                "Password reset email sent",
                extra={"email": email}
            )

        except Exception:
            logger.exception(
                "Failed to send password reset email",
                extra={"email": email}
            )
                