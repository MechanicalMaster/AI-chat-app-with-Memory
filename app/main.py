import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app.api.routes import router
from app.core.config import settings
from pathlib import Path

app = FastAPI(title="Channel Finance Assistant")

# CORS middleware with Railway-specific configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the absolute path to the static directory
BASE_DIR = Path(__file__).resolve().parent
static_dir = BASE_DIR / "static"
templates_dir = BASE_DIR / "templates"

# Mount static files with absolute path
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Templates with absolute path
templates = Jinja2Templates(directory=str(templates_dir))

# Include API routes
app.include_router(router)

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/static/{file_path:path}")
async def serve_static(file_path: str):
    file_location = static_dir / file_path
    if not file_location.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_location)

@app.get("/health")
async def health_check():
    """Health check endpoint for Railway"""
    return {"status": "healthy"}

# Get port from Railway environment
port = int(os.getenv("PORT", 8000)) 