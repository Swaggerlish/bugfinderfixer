import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import analyze

app = FastAPI(
    title="Bug Finder & Fixer API",
    description="API for analyzing code and finding bugs",
    version="1.0.0"
)

# Get allowed origins from environment variable or use defaults
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:3001,https://your-app.vercel.app"
).split(",")

# Configure CORS - supports multiple origins for development and production
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # Configurable via environment variable
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analyze.router, prefix="/api", tags=["analyze"])

@app.get("/")
async def root():
    return {
        "message": "Bug Finder & Fixer API",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Made with Bob
