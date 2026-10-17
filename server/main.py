from fastapi import FastAPI
from database import init_db
from fetch_data import update_stops

app = FastAPI()

init_db()
update_stops()

@app.get("/")
async def root():
    return {"message": "Hello World"}