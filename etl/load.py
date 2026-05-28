from sqlalchemy import create_engine, text
from loguru import logger
from config import DB_PATH

def get_engine():
    return create_engine(f"sqlite:///{DB_PATH}")

def create_table_if_not_exists(engine):
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS exchange_rates(
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                date        TEXT NOT NULL,
                currency    TEXT NOT NULL,
                rate        REAL NOT NULL,
                unit        INTEGER NOT NULL,
                UNIQUE(date, currency)
            )
        """))
        conn.commit()


def load_records(records: list[dict]):
    if not records:
        logger.warning("Nincs betöltendő rekord")
        return
    
    engine = get_engine()
    create_table_if_not_exists(engine)

    inserted = 0
    skipped = 0

    with engine.connect() as conn:
        for record in records:
            result = conn.execute(text("""
                INSERT OR IGNORE INTO exchange_rates (date, currency, rate, unit)
                VALUES (:date, :currency, :rate, :unit)
            """), record)

            if result.rowcount > 0:
                inserted += 1
            else:
                skipped += 1

        conn.commit()

    logger.success(f"Betöltés kész: {inserted} új rekord, {skipped} kihagyva (már létezettt).")