import os
from fastapi_mail import ConnectionConfig
from dotenv import load_dotenv

load_dotenv()

MAIL_USER = os.getenv("EMAIL_USERNAME")
MAIL_PASS = os.getenv("EMAIL_PASSWORD")
MAIL_FRM = os.getenv("EMAIL_FROM")
FRONTEND_URL = os.getenv("FRONTEND_URL")

mail_conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USER,
    MAIL_PASSWORD=MAIL_PASS,
    MAIL_FROM=MAIL_FRM,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)