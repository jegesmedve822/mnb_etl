# MNB ETL Pipeline

Napi árfolyamokat kér le az MNB SOAP API-jából, és tölti be lokális SQLite adatbázisba

**Valuták:** EUR, USD, GBP, CHF
**Adatforrás:** [MNB Árfolyam API](https://mnb.hu/arfolyamok.asmx)

---

## Indítás klónozás után

### 1. Klónozd a repót
```bash
git clone https://github.com/FELHASZNÁLÓNÉV/mnb-etl.git
cd mnb-etl
```

### 2. Futtasd a setup scriptet
```bash
chmod +x setup.sh
./setup.sh
```

### 3. Aktiváld a virtuális környezetet
```bash
source venv/bin/activate
```

### 4. Futtasd az ETL-t

Egyszeri futtatás (teszteléshez):
```bash
python main.py --now
```

Scheduler indítása (naponta automatikusan fut):
```bash
python main.py
```
> A scheduler alapból **08:00-kor** fut — ez a `config.py`-ban módosítható.

---

## Konfiguráció

A `config.py`-ban állítható:
- `CURRENCIES` — lekérendő valuták listája
- `SCHEDULE_TIME` — napi futás időpontja (24h formátum)
- `DB_PATH` — adatbázis fájl helye

---


## Projekt struktúra

mnb-etl/
├── etl/
│   ├── extract.py      # MNB API hívás
│   ├── transform.py    # XML feldolgozás
│   ├── load.py         # SQLite betöltés
│   └── pipeline.py     # ETL összekötése
├── scheduler/
│   └── cron.py         # Napi scheduler
├── db/                 # SQLite adatbázis (gitignore-olva)
├── logs/               # Log fájlok (gitignore-olva)
├── config.py           # Beállítások
├── main.py             # Belépési pont
├── setup.sh            # Egyszerű telepítő script
└── requirements.txt

