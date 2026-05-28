import sys
from loguru import logger
from etl.pipeline import run_pipeline
from scheduler.cron import start_scheduler

logger.add("logs/etl.log", rotation="1 week", retention="1 month")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--now":
        logger.info("Egyszeri futtatás módban indult.")
        run_pipeline()
    else:
        start_scheduler()