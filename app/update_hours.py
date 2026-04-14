from datetime import date

@router.post("/admin/update_hours")
async def update_hours(
    X_Admin_Token: str = Header(..., alias="X-Admin-Token")
):
    print("TOKEN RECEIVED:", X_Admin_Token)
    print("TOKEN EXPECTED:", HOURS_SECRET)

    if X_Admin_Token != HOURS_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")

    today = date.today().strftime("%Y-%m-%d")
    print("FETCHING HOURS FOR:", today)

    hours = scrape_hours(today)

    print("SCRAPED HOURS:")
    print(json.dumps(hours, indent=2))

    cached_hours.clear()
    cached_hours.update({"units": hours})

    with open("hours.json", "w") as f:
        json.dump(cached_hours, f)

    return {"status": "ok", "units": len(hours)}
