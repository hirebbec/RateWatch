from prefect import flow

from tasks.golden import get_silver_rows, transform_to_gold, load_gold


@flow(name="golden-flow")
async def golden_flow(object_key: str) -> None:
    silver_rows = await get_silver_rows(
        object_key=object_key,
    )

    rows = await transform_to_gold(
        silver_rows=silver_rows,
    )

    await load_gold(rows)
