from datetime import datetime, timezone


def build_bronze_rates_key() -> str:
    timestamp = int(datetime.now(timezone.utc).timestamp())

    return f"rates/{timestamp}.html"
