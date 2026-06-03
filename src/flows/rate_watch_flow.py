from prefect import flow


@flow(name="exchange-rates-pipeline")
async def rate_rates_flow(base_currency: str = "USD"):
    bronze_object_key = await bronze_exchange_rates_flow(base_currency)