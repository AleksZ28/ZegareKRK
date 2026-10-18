from fastapi import FastAPI
from database import init_db
from fetch_data import update_gtfs_static, fetch_departures, get_departures_from_stop
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    update_gtfs_static()
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_gtfs_static, 'cron', hour=3, minute=0)
    scheduler.start()

    try:
        yield
    finally:
        scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return fetch_departures()

@app.get("/departures/{stop_id}")
async def get_departures(stop_id: str):
    return get_departures_from_stop(stop_id)