print(">>> USING CORRECT MAIN.PY <<<")

from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.app_router import route_request
from app.state import cached_hours   # <-- import shared state

app = FastAPI()

HOURS_SECRET = "your-secret-token"   # <-- define your secret here

# -----------------------------
# Normalized Pydantic Models
# -----------------------------

class HourBlock(BaseModel):
    label: str
    open_time: str
    close_time: str

class UnitHours(BaseModel):
    unit_id: str
    name: str
    about_url: Optional[str]
    menu_url: Optional[str]
    hours: List[HourBlock]


# -----------------------------
# Endpoints
# -----------------------------

@app.post("/admin/update_hours")
async def update_hours(request: Request, units: List[UnitHours]):
    token = request.headers.get("X-Admin-Token")
    if token != HOURS_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")

    #data = await request.json()

    # update the shared hours store
    cached_hours.clear()
    cached_hours.update({"units": [u.dict() for u in units]})

    return {"status": "ok", "units": len(units)}

class Query(BaseModel):
    message: str
    
@app.post("/ask")
def ask(query: Query):
    return {"response": route_request(query.message)}
    
@app.get("/debug/hours")
def debug_hours():
    return cached_hours
