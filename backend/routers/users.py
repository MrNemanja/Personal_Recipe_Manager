from fastapi import APIRouter, Path, HTTPException, Depends, Cookie, Request
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.orm import Session
from database import get_db
from models import User, Recipe, RefreshToken
from schemas import CreateUser, UserResponse, RecipeResponse, LoginUser, VerifyEmail, ResendEmail, ForgotPasswordRequest, ResetPasswordRequest, MfaSetupRequest, MfaVerifyRequest
from passlib.context import CryptContext
from auth import create_access_token, create_refresh_token, create_mfa_token, verify_mfa_token, delete_expired_refresh_tokens, get_current_user_optional, get_current_user
from services.email_service import send_verification_email, send_reset_password_email
from services.brute_force import check_login_limits, reset_login_attempts
from typing import Optional
from datetime import datetime, timedelta
import secrets
import pyotp
import qrcode
import io
import os
from jose import jwt

# Routes for managing users and their favorite recipes
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

# GET -> get current user
@router.get("/me", response_model=Optional[UserResponse])
def get_me(current_user: Optional[User] = Depends(get_current_user_optional)):

    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return current_user

# GET /{id} -> get user by ID
@router.get("/{id}", response_model=UserResponse)
def get_user(id: int = Path(description="The ID of the user you want to view", gt=0), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

# POST /register -> create a new user with hashed password
@router.post("/register")
async def register_user(user: CreateUser, db: Session = Depends(get_db)):
    if db.query(User).filter((User.username == user.username) | (User.email == user.email)).first():
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = pwd_context.hash(user.password)
    token = secrets.token_urlsafe(32)

    new_user = User(
        username=user.username, 
        password_hash=hashed_password, 
        email=user.email, 
        role=user.role,
        is_verified=False,
        verification_token=token, 
        verification_token_expires_at = datetime.utcnow() + timedelta(minutes=30),
        reset_password_token=None,
        reset_password_token_expires_at = None,
        favorite_recipe_id=None
        )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    await send_verification_email(new_user.email, token)

    return {"message" : "Registration successful. Please check your email to verify your account."}

#POST /verify-email -> email verification for registered users
@router.post("/verify-email")
async def verify_email(token: VerifyEmail, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.verification_token == token.token).first()

    if not user:
        raise HTTPException( status_code=400, detail="Invalid or used verification link")

    if user.verification_token_expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Verification link has expired")


    user.is_verified = True
    user.verification_token = None
    user.verification_token_expires_at = None

    db.commit()

    return {"message": "Email successfully verified"}

#POST /resend-verification -> resend email verification for registered users
@router.post("/resend-verification")
async def resend_verification(email: ResendEmail, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email.email).first()

    if not user or user.is_verified:
        return {
            "message": "If the account exists, a verification email has been sent."
        }

    new_token = secrets.token_urlsafe(32)
    user.verification_token = new_token
    user.verification_token_expires_at = datetime.utcnow() + timedelta(minutes=30)
    
    db.commit()

    await send_verification_email(user.email, new_token)

    return {
        "message": "If the account exists, a verification email has been sent."
    }


# POST /login -> Log in into your account
@router.post("/login")
async def login_user(login_user: LoginUser, request: Request, db: Session = Depends(get_db)):

    ip = request.client.host

    #Brute force check
    check_login_limits(login_user.username, ip)

    user = db.query(User).filter(User.username == login_user.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not pwd_context.verify(login_user.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not user.is_verified:
        raise HTTPException(
            status_code=403,
            detail="Please verify your email before logging in"
        )

    reset_login_attempts(login_user.username)

    if user.mfa_enabled:
        if not user.mfa_last_verified or datetime.utcnow() - user.mfa_last_verified > timedelta(days=7):
            temp_token = create_mfa_token({"user_id": user.id, "mfa_pending": True, "type": "mfa"})
            return {"mfa_required": True, "mfa_token": temp_token}

    access_token = create_access_token({"user_id": user.id, "type" : "access"})
    refresh_token = create_refresh_token(user, db)

    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=True,
        samesite="none",
        max_age=1800
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=604800
    )

    return response

#POST /mfa/setup make secret key and generate qrcode
@router.post("/mfa/setup")
def mfa_setup(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == current_user.userId).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.mfa_enabled:
        raise HTTPException(400, "MFA already enabled")

    secret = pyotp.random_base32()
    user.mfa_secret = secret
    db.commit()
    db.refresh(user)

    uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=user.username,
        issuer_name="MyRecipeApp"
    )

    qr = qrcode.make(uri)
    buf = io.BytesIO()
    qr.save(buf, format='PNG')
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")

#POST /mfa/verify-setup Called only once, after enabling mfa
@router.post("/mfa/verify-setup")
def verify_mfa_setup(data: MfaSetupRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == current_user.userId).first()
    if not user or not user.mfa_secret:
        raise HTTPException(status_code=400, detail="MFA not setup")

    totp = pyotp.TOTP(user.mfa_secret)
    if not totp.verify(data.code):
        raise HTTPException(status_code=401, detail="Invalid MFA code")

    user.mfa_enabled = True
    user.mfa_last_verified = datetime.utcnow()
    db.commit()

    return {"message": "MFA enabled successfully"}


#POST /mfa/verify verification of the code of 6 digits
@router.post("/mfa/verify-login")
def verify_mfa(data: MfaVerifyRequest, db: Session = Depends(get_db)):

    try:
        user_id = verify_mfa_token(data.mfa_token)
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired MFA token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.mfa_secret:
        raise HTTPException(status_code=400, detail="MFA not setup")

    totp = pyotp.TOTP(user.mfa_secret)
    if not totp.verify(data.code):
        raise HTTPException(status_code=401, detail="Invalid MFA code")

    user.mfa_last_verified = datetime.utcnow()
    db.commit()
    db.refresh(user)

    access_token = create_access_token({"user_id": user.id, "type" : "access"})
    refresh_token = create_refresh_token(user, db)

    response = JSONResponse({"message": "Login successful"})
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=True,
        samesite="none",
        max_age=1800
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=604800
    )

    return response


#POST /refresh -> Create new access token using refresh token
@router.post("/refresh")
async def refresh_token_endpoint(refresh_token: str = Cookie(None), db: Session = Depends(get_db)):

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    delete_expired_refresh_tokens(db)

    token_obj = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not token_obj or token_obj.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user = token_obj.user

    # Rotate refresh token for security
    db.delete(token_obj)
    db.commit()
    new_refresh_token = create_refresh_token(user, db)

    access_token = create_access_token({"user_id": token_obj.user_id, "type" : "access"})

    response = JSONResponse(content={"message": "Access token refreshed"})
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=True,
        samesite="none",
        max_age=1800
    )
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=604800
    )
    return response

#POST /forgot-password -> Send a forgot password form link to user email
@router.post("/forgot-password")
async def forgot_password(email: ForgotPasswordRequest, db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.email == email.email).first()

    if user and user.is_verified:
        token = secrets.token_urlsafe(32)
        user.reset_password_token = token
        user.reset_password_token_expires_at = datetime.utcnow() + timedelta(minutes=30)
        db.commit()

        await send_reset_password_email(user.email, token)

    return {
        "message": "If the account exists, a password reset email has been sent."
    }

#POST /reset-password -> Reset your password
@router.post("/reset-password")
async def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    
    user = db.query(User).filter(
        User.reset_password_token == data.token
    ).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    if user.reset_password_token_expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Reset token has expired")

    user.password_hash = pwd_context.hash(data.new_password)

    user.reset_password_token = None
    user.reset_password_token_expires_at = None

    db.commit()

    return {"message": "Password has been successfully reset"}

# POST /logout -> Log out and return to home page
@router.post("/logout")
def logout_user(refresh_token: str = Cookie(None), db: Session = Depends(get_db)):

    if refresh_token:
        token_obj = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
        if token_obj:
            db.delete(token_obj)
            db.commit()

    response = JSONResponse(content={"message": "Logged out successfully"})
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return response

# GET /{user_id}/favorite -> get user's favorite recipe
@router.get("/{user_id}/favorite", response_model=RecipeResponse)
def get_favorite_recipe(user_id: int = Path(description="The ID of the user whose favorite recipe you want to see", gt=0),
                        db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user:
        if user.favorite_recipe_id is None:
            raise HTTPException(status_code=404, detail="User has no favorite recipe")
        else:
            return user.favorite_recipe
    else:
        raise HTTPException(status_code=404, detail="User not found")

# POST /{user_id}/favorite/{recipe_id} -> mark a recipe as favorite for user
@router.post("/{user_id}/favorite/{recipe_id}")
def mark_favorite_recipe(user_id: int = Path(description="The ID of the user you want to tag a favorite recipe to", gt=0),
                         recipe_id: int = Path(description="The ID of the recipe you want to mark as a favorite", gt=0)
                         , db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    elif not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    user.favorite_recipe_id = recipe_id
    db.commit()
    db.refresh(recipe)

    return {"message": "Recipe marked as favorite"}

# PUT /{user_id}/favorite/{new_recipe_id} -> change user's favorite recipe
@router.put("/{user_id}/favorite/{new_recipe_id}")
def update_favorite_recipe(user_id: int = Path(description="The ID of the user you want to change a favorite recipe", gt=0),
                         new_recipe_id: int = Path(description="The ID of the new recipe you want to mark as a favorite", gt=0)
                         , db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    recipe = db.query(Recipe).filter(Recipe.id == new_recipe_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    elif not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    user.favorite_recipe_id = new_recipe_id
    db.commit()
    db.refresh(recipe)

    return {"message": "New recipe marked as favorite"}

# DELETE /{user_id}/favorite -> remove user's favorite recipe
@router.delete("/{user_id}/favorite")
def delete_favorite_recipe(user_id: int = Path(description="The ID of the user whose favorite recipe you want to delete", gt=0),
                           db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.favorite_recipe_id = None
    db.commit()
    db.refresh(user)

    return {"message": "Favorite recipe deleted"}
