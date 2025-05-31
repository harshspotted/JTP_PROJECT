from fastapi import Depends, FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from routes import predict, analysis

from settings import settings


# App definition
app = FastAPI(
    title="JTP: ML Inference Pod for Project Recommender",
    description="JTP: ML Inference Pod for Project Recommender",
)

# Adding CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,  # You can restrict this to specific origins
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# Health Check
@app.get("/", tags=["Health"])
def root():
    return {"message": "Welcome to JTP: ML Inference Pod for Project Recommender!"}


# Routers
app.include_router(predict.router)
app.include_router(analysis.router)
