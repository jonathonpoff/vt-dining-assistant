from fastapi import FastAPI
from pydantic import BaseModel
from app.app_router import route_request
#
app = FastAPI()
#
class Query(BaseModel):
    message: str
#
@app.post("/ask")
def ask(query: Query):
    return {"response": route_request(query.message)}
