from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

app = FastAPI(title=settings.PROJECT_NAME)

# Trust Proxy Headers (for Fly.io SSL termination)
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to Car Rental Platform API"}

from app.api.v1.api import api_router
app.include_router(api_router, prefix=settings.API_V1_STR)
