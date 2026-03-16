print(">>> USING CORRECT MAIN.PY <<<")

from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from app.app_router import route_request
from app.state import cached_hours   # <-- import shared state

app = FastAPI()

HOURS_SECRET = "your-secret-token"   # <-- define your secret here

@app.post("/admin/update_hours")
async def update_hours(request: Request):
    token = request.headers.get("X-Admin-Token")
    if token != HOURS_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")

    data = await request.json()

    # update the shared hours store
    cached_hours.clear()
    cached_hours.update({"units": data})

    return {"status": "ok", "units": len(data)}

class Query(BaseModel):
    message: str

@app.post("/ask")
def ask(query: Query):
    return {"response": route_request(query.message)}
