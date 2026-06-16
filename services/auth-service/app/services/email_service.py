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


        html_content = f"""
        <!DOCTYPE html>
        <html>
        <body style="margin:0;padding:0;background:#f4f7fb;font-family:Arial,sans-serif;">

            <div style="max-width:600px;margin:40px auto;background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,0.08);">

                <div style="background:linear-gradient(135deg,#ef4444,#dc2626);padding:32px;text-align:center;color:white;">
                    <h1 style="margin:0;font-size:28px;">
                        🔐 Password Reset Request
                    </h1>

                    <p style="margin-top:10px;font-size:15px;">
                        AI Interview Platform
                    </p>
                </div>

                <div style="padding:35px;">

                    <h2 style="color:#111827;">
                        Reset Your Password
                    </h2>

                    <p style="color:#4b5563;line-height:1.8;">
                        We received a request to reset your password.
                        Click the button below to create a new password.
                    </p>

                    <div style="text-align:center;margin:35px 0;">
                        <a
                            href="{reset_link}"
                            style="
                                background:#ef4444;
                                color:white;
                                text-decoration:none;
                                padding:14px 28px;
                                border-radius:10px;
                                font-size:16px;
                                font-weight:bold;
                                display:inline-block;
                            "
                        >
                            Reset Password
                        </a>
                    </div>

                    <div style="
                        background:#fef2f2;
                        border-left:4px solid #ef4444;
                        padding:16px;
                        border-radius:8px;
                        margin-bottom:25px;
                    ">
                        <p style="margin:0;color:#991b1b;">
                            ⏳ This reset link will expire in
                            <strong>15 minutes</strong>.
                        </p>
                    </div>

                    <p style="color:#6b7280;line-height:1.7;">
                        If you did not request a password reset,
                        you can safely ignore this email.
                        Your account remains secure.
                    </p>

                    <hr style="margin:30px 0;border:none;border-top:1px solid #e5e7eb;">

                    <p style="font-size:12px;color:#9ca3af;word-break:break-all;">
                        If the button above doesn't work, copy and paste this URL into your browser:
                        <br><br>
                        {reset_link}
                    </p>

                </div>

                <div style="
                    background:#f9fafb;
                    padding:18px;
                    text-align:center;
                    font-size:12px;
                    color:#9ca3af;
                ">
                    © 2026 AI Interview Platform
                    <br>
                    Secure Authentication System
                </div>

            </div>

        </body>
        </html>
        """

        params = {
            "from": settings.EMAIL_FROM,
            "to": [email],
            "subject": "🔐 Reset Your Password - AI Interview Platform",
            "html": html_content,
        }

        try:
            resend.Emails.send(params)

            logger.info(
                "Password reset email sent successfully",
                extra={"email": email}
            )

        except Exception:
            logger.exception(
                "Failed to send password reset email",
                extra={"email": email}
            )
            raise

