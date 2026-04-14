from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from app.app_router import route_request
from app.state import cached_hours

# Create FastAPI app
app = FastAPI()

# Import routers AFTER app is created
from app.update_hours import router as hours_router
app.include_router(hours_router)


# -----------------------------
# Models for /ask endpoint
# -----------------------------

class Query(BaseModel):
    message: str


# -----------------------------
# Endpoints
# -----------------------------

@app.post("/ask")
def ask(query: Query):
    return {"response": route_request(query.message)}


@app.get("/debug/hours")
def debug_hours():
    return cached_hours
