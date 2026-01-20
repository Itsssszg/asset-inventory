from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.api.v1.api import api_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine


app = FastAPI(title="Asset Inventory API")

# Create database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

if settings.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"] ,
        allow_headers=["*"] ,
    )

app.include_router(api_router, prefix="/api/v1")
