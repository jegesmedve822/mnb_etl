import schedule
import time
from loguru import logger
from config import SCHEDULE_TIME
from etl.pipeline import run_pipeline


def start_scheduler():
    logger.info(f"Scheduler indul. Napi futás: {SCHEDULE_TIME}")

    schedule.every().day.at(SCHEDULE_TIME).do(run_pipeline)

    while True:
        schedule.run_pending()
        time.sleep(30)