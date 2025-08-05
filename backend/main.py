from fastapi import FastAPI
from backend.database import engine, Base
from backend.routes import user_routes, task_routes

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Include Routers
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(task_routes.router, prefix="/tasks", tags=["Tasks"])
