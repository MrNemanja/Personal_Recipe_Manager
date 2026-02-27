from fastapi import FastAPI
from database import Base, engine
from routers.recipes import router as recipes_router
from routers.users import router as users_router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from seed import seed_admin
from pathlib import Path

# Create all tables in the database if they do not exist
Base.metadata.create_all(bind=engine)

#Seed Admin
seed_admin()

# Start-up for FastAPI
app = FastAPI()

#
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers for recipes and users
app.include_router(recipes_router)
app.include_router(users_router)
Path("uploads/profiles").mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")



