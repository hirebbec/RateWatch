from datetime import datetime, timezone


def build_bronze_rates_key(base_currency: str) -> str:
    timestamp = int(datetime.now(timezone.utc).timestamp())

    return f"rates/{base_currency}/{timestamp}.json"