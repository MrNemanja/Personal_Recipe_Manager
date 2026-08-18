import httpx
from config import FRONTEND_URL, BREVO_API_KEY, MAIL_FROM, MAIL_FROM_NAME
import os

BREVO_URL = "https://api.brevo.com/v3/smtp/email"

async def send_email(to_email: str, subject: str, html_content: str):

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json",
    }

    payload = {
        "sender": {
            "name": MAIL_FROM_NAME,
            "email": MAIL_FROM,
        },
        "to": [
            {
                "email": to_email,
            }
        ],
        "subject": subject,
        "htmlContent": html_content,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            BREVO_URL,
            headers=headers,
            json=payload,
        )

    response.raise_for_status()


async def send_verification_email(to_email: str, token: str):

    verification_link = f"{FRONTEND_URL}/verify-email?token={token}"

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Verify your email</title>
</head>

<body style="margin:0; padding:0; background-color:#f4f4f4; font-family:Arial, sans-serif;">

  <table width="100%" cellpadding="0" cellspacing="0">
    <tr>
      <td align="center" style="padding:40px 0;">

        <table width="600" cellpadding="0" cellspacing="0"
               style="background:#ffffff; border-radius:8px; padding:30px;">

          <tr>
            <td style="text-align:center;">
              <h2 style="color:#222;">Verify your email address</h2>
            </td>
          </tr>

          <tr>
            <td style="padding:20px 0; color:#555; font-size:15px;">
              Hi,<br><br>
              Thank you for signing up!
              Please confirm your email address by clicking the button below.
            </td>
          </tr>

          <tr>
            <td align="center" style="padding:20px 0;">

              <a href="{verification_link}"
                 style="background:#FF8C42; color:#ffffff; text-decoration:none;
                        padding:12px 24px; border-radius:6px; font-weight:bold;">
                Verify Email
              </a>

            </td>
          </tr>

          <tr>
            <td style="padding-top:20px; color:#777; font-size:14px;">
              This link will expire in <strong>30 minutes</strong>.<br><br>
              If you did not create this account, you can safely ignore this email.
            </td>
          </tr>

          <tr>
            <td style="padding-top:30px; color:#999; font-size:13px; text-align:center;">
              © Recipe Manager · All rights reserved
            </td>
          </tr>

        </table>

      </td>
    </tr>
  </table>

</body>
</html>
"""

    await send_email(
        to_email,
        "Verify your email",
        html_content,
    )


async def send_reset_password_email(to_email: str, token: str):

    password_reset_link = f"{FRONTEND_URL}/reset-password?token={token}"

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Reset your password</title>
</head>

<body style="margin:0; padding:0; background-color:#f4f4f4; font-family:Arial, sans-serif;">

  <table width="100%" cellpadding="0" cellspacing="0">
    <tr>
      <td align="center" style="padding:40px 0;">

        <table width="600" cellpadding="0" cellspacing="0"
               style="background:#ffffff; border-radius:8px; padding:30px;">

          <tr>
            <td style="text-align:center;">
              <h2 style="color:#222;">Reset your password</h2>
            </td>
          </tr>

          <tr>
            <td style="padding:20px 0; color:#555; font-size:15px;">
              Hi,<br><br>
              We received a request to reset your password.
              Click the button below to create a new one.
            </td>
          </tr>

          <tr>
            <td align="center" style="padding:20px 0;">

              <a href="{password_reset_link}"
                 style="background:#FF8C42; color:#ffffff; text-decoration:none;
                        padding:12px 24px; border-radius:6px; font-weight:bold;">
                Reset Password
              </a>

            </td>
          </tr>

          <tr>
            <td style="padding-top:20px; color:#777; font-size:14px;">
              This link will expire in <strong>30 minutes</strong>.<br><br>
              If you did not request a password reset, you can safely ignore this email.
            </td>
          </tr>

          <tr>
            <td style="padding-top:30px; color:#999; font-size:13px; text-align:center;">
              © Recipe Manager · All rights reserved
            </td>
          </tr>

        </table>

      </td>
    </tr>
  </table>

</body>
</html>
"""

    await send_email(
        to_email,
        "Reset your password",
        html_content,
    )