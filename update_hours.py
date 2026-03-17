from pydantic import BaseModel
from typing import List, Optional
from fastapi import Body, Request, HTTPException
import json

class HourBlock(BaseModel):
    label: str
    open_time: str
    close_time: str

class UnitHoursNormalized(BaseModel):
    unit_id: str
    name: str
    about_url: Optional[str]
    menu_url: Optional[str]
    hours: List[HourBlock]

@app.post("/admin/update_hours")
async def update_hours(
    request: Request,
    units: List[UnitHoursNormalized] = Body(...)
):
    token = request.headers.get("X-Admin-Token")
    if token != HOURS_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # update in-memory cache
    cached_hours.clear()
    cached_hours.update({"units": [u.dict() for u in units]})
    
    # write to file for persistence
    with open("hours.json", "w") as f:
        json.dum(cached_hours, f)
        
    return {"status": "ok", "units": len(units)}
