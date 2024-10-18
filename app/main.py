from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import events
# from app.core.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="http://localhost:3000",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include event router
app.include_router(events.router)
