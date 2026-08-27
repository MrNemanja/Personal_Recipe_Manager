from pathlib import Path
import secrets
import os
import shutil
from fastapi import UploadFile, HTTPException

UPLOAD_DIR_PROFILE = Path(os.getenv("UPLOAD_DIR_PROFILE", "uploads/profiles"))
UPLOAD_DIR_RECIPES = Path(os.getenv("UPLOAD_DIR_RECIPES", "uploads/recipe_images"))
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def save_profile_image(profile_image: UploadFile) -> str:
    ext = profile_image.filename.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")

    profile_image.file.seek(0, 2)
    file_size = profile_image.file.tell()
    profile_image.file.seek(0)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    filename = f"user_{secrets.token_hex(8)}.{ext}"
    file_path = UPLOAD_DIR_PROFILE / filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(profile_image.file, buffer)

    return f"uploads/profiles/{filename}"

def save_recipe_image(recipe_image: UploadFile) -> str:
    ext = recipe_image.filename.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")

    recipe_image.file.seek(0, 2)
    file_size = recipe_image.file.tell()
    recipe_image.file.seek(0)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    filename = f"recipe_{secrets.token_hex(8)}.{ext}"
    file_path = UPLOAD_DIR_RECIPES / filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(recipe_image.file, buffer)

    return f"uploads/recipe_images/{filename}"

def delete_image(image_path: str | None):
    if not image_path:
        return

    file_path = Path(image_path)

    if file_path.exists():
        file_path.unlink()