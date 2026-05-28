import requests
from datetime import date
from loguru import logger
from config import MNB_WSDL, CURRENCIES


def fetch_exchange_rates(target_date: date = None) -> str:
    if target_date is None:
        target_date = date.today()

    date_str = target_date.strftime("%Y-%m-%d")
    currencies_str = ",".join(CURRENCIES)

    soap_body = f"""<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
            <GetExchangeRates xmlns="http://www.mnb.hu/webservices/">
            <startDate>{date_str}</startDate>
            <endDate>{date_str}</endDate>
            <currencyNames>{currencies_str}</currencyNames>
            </GetExchangeRates>
        </soap:Body>
        </soap:Envelope>"""

    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": "http://www.mnb.hu/webservices/MNBArfolyamServiceSoap/GetExchangeRates"
    }

    logger.info(f"Adatlekérés: {date_str}, valuták: {currencies_str}")

    try:
        response = requests.post(
            "http://www.mnb.hu/arfolyamok.asmx",
            data=soap_body.encode("utf-8"),
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        logger.success(f"Sikeres lekérés: {date_str}")
        return response.text

    except requests.RequestException as e:
        logger.error(f"API hiba: {e}")
        raise