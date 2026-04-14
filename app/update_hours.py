from fastapi import APIRouter, Header, HTTPException, Request
from typing import Optional
from app.scrapers.hours import scrape_hours
from app.state import cached_hours
import json

router = APIRouter()

HOURS_SECRET = "your-secret-token"

@router.post("/admin/update_hours")
async def update_hours(
    X_Admin_Token: str = Header(..., alias="X-Admin-Token")
):
    print("TOKEN RECEIVED:", X_Admin_Token)
    print("TOKEN EXPECTED:", HOURS_SECRET)

    if X_Admin_Token != HOURS_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")

    hours = scrape_hours("2026-04-13")

    print("SCRAPED HOURS:")
    print(json.dumps(hours, indent=2))

    cached_hours.clear()
    cached_hours.update({"units": hours})

    with open("hours.json", "w") as f:
        json.dump(cached_hours, f)

    return {"status": "ok", "units": len(hours)}
