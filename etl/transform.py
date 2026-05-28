import xml.etree.ElementTree as ET
from loguru import logger

NS = {
    "soap": "http://schemas.xmlsoap.org/soap/envelope/",
    "mnb":  "http://www.mnb.hu/webservices/"
}


def parse_exchange_rates(xml_string: str) -> list[dict]:
    """
    Feldolgozza az MNB API nyers SOAP XML válaszát.
    Visszaad egy listát szótárakból, pl.:
    [
        {"date": "2024-01-15", "currency": "EUR", "rate": 382.45, "unit": 1},
        ...
    ]
    """
    if not xml_string:
        logger.warning("Üres XML, nincs mit feldolgozni.")
        return []

    records = []

    try:
        root = ET.fromstring(xml_string)

        result_node = root.find(".//mnb:GetExchangeRatesResult", NS)

        if result_node is None or not result_node.text:
            logger.warning("Nem található GetExchangeRatesResult az XML-ben.")
            return []

        inner_xml = ET.fromstring(result_node.text)

        for day in inner_xml.findall("Day"):
            day_date = day.attrib.get("date")

            for rate_elem in day.findall("Rate"):
                currency = rate_elem.attrib.get("curr")
                unit = int(rate_elem.attrib.get("unit", 1))
                rate = float(rate_elem.text.replace(",", "."))

                records.append({
                    "date": day_date,
                    "currency": currency,
                    "rate": rate,
                    "unit": unit
                })

        logger.success(f"{len(records)} rekord feldolgozva.")
        return records

    except ET.ParseError as e:
        logger.error(f"XML parse hiba: {e}")
        raise