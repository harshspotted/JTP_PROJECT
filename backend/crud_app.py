from fastapi import Depends, FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from routes import crud
from settings import settings


# App definition
app = FastAPI(
    title="JTP: CRUD Pod for Project Recommender",
    description="JTP: CRUD Pod for Project Recommender",
)

# Adding CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,  # You can restrict this to specific origins
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# @app.on_event("startup")
# async def on_startup():
#     FastAPICache.init(InMemoryBackend())


# Health Check
@app.get("/", tags=["Health"])
def root():
    return {"message": "Welcome to JTP: CRUD Pod for Project Recommender!"}


# Routers
app.include_router(crud.router)
