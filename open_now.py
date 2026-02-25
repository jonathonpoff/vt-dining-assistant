import json
with open("Location_Hours.json", "r") as f:
    locations = json.load(f)
    
    from datetime import datetime
    
    def get_open_locations(now, locations):
        weekday = now.strftime("%a").lower()[:3]
        current_time = now.strftime("%H:%M")
        
        open_locations = []
        
        for loc in locations:
            hours = loc.get("hours",{})
            if weekday not in hours:
                continue
              
            for window in hours [weekday]:
                if window["open"] <= current_time <= window["close"]:
                    open_locations.append(loc)
                    break
                    
            return open_locations