from fastapi import HTTPException
from redis_client import r
import os

#Borders
username_limit = int(os.getenv("USERNAME_LIMIT"))
ip_limit = int(os.getenv("IP_LIMIT"))

#Check if there is any login limits
def check_login_limits(username : str, ip : str):

    username_key = f"login:email:{username}"
    ip_key = f"login:ip:{ip}"

    username_attempts = r.get(username_key)
    ip_attempts = r.get(ip_key)

    if username_attempts and int(username_attempts) >= username_limit:
        raise HTTPException(429, "Account temporarily locked")

    if ip_attempts and int(ip_attempts) >= ip_limit:
        raise HTTPException(429, "To many requests from this IP")

    r.incr(username_key)
    r.expire(username_key, 600)

    r.incr(ip_key)
    r.expire(ip_key, 300)

# Reset after successfull login
def reset_login_attempts(username : str):
    r.delete(f"login:email:{username}")

