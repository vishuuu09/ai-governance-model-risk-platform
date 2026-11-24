from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import Base, engine
from app import models
from app.routes import router

app = FastAPI(title=settings.APP_NAME, version="1.0.0",
              description="AI model inventory, risk assessment and governance workflow API")
app.add_middleware(CORSMiddleware, allow_origins=[settings.FRONTEND_ORIGIN],
    allow_credentials=True, allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"])
if settings.ENVIRONMENT == "development":
    Base.metadata.create_all(bind=engine)  # Replace with Alembic migrations before deployment.
app.include_router(router, prefix=settings.API_V1_PREFIX)
@app.get("/")
def root():
    return {"message": "AI Governance Platform API", "docs": "/docs"}
