from fastapi import FastAPI
from database import init_db
from fetch_data import update_gtfs_static
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
    return {"message": "Hello World"}