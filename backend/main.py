from fastapi import FastAPI
from database import Base, engine
from routers.recipes import router as recipes_router
from routers.users import router as users_router

# Create all tables in the database if they do not exist
Base.metadata.create_all(bind=engine)

# Start-up for FastAPI
app = FastAPI()

# Include routers for recipes and users
app.include_router(recipes_router)
app.include_router(users_router)



