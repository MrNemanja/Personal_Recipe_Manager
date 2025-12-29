from fastapi_mail import FastMail, MessageSchema
from config import mail_conf, FRONTEND_URL

fm = FastMail(mail_conf)

async def send_verification_email(to_email: str, token: str):
    
    verification_link = f"{FRONTEND_URL}/verify-email?token={token}" 

    message = MessageSchema(
        subject = "Verify your email",
        recipients = [to_email],
        body = f"""
Hi,

Please verify your email by clicking the link below:

{verification_link}

If you didn’t create this account, ignore this email.
""",
        subtype = "plain"
    )

    await fm.send_message(message)