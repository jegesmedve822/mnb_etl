from loguru import logger
from datetime import date
from etl.extract import fetch_exchange_rates
from etl.transform import parse_exchange_rates
from etl.load import load_records

def run_pipeline(target_date: date = None):

    logger.info("=" * 40)
    logger.info("ETL pipeline indul...")

    #1. Extract
    raw_xml = fetch_exchange_rates(target_date)

    #2. Transform
    records = parse_exchange_rates(raw_xml)

    #3. Load
    load_records(records)

    logger.info("ETL pipeline sikeresen lefutott.")
    logger.info("=" * 40)    