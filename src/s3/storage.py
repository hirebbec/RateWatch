from contextlib import asynccontextmanager
from typing import AsyncIterator

from aiobotocore.client import AioBaseClient
from botocore.exceptions import ClientError
from fastapi import Depends
from loguru import logger

from core.config import settings
from s3.client import get_s3_client, s3_client_context


class S3Storage:
    def __init__(self, s3_client: AioBaseClient = Depends(get_s3_client)) -> None:
        self._s3_client = s3_client
        self._s3_bucket_name = settings().MINIO_DEFAULT_BUCKET

    async def get_file(self, full_key: str) -> bytes:
        key = full_key.removeprefix(self._s3_bucket_name)

        try:
            response = await self._s3_client.get_object(
                Bucket=self._s3_bucket_name,
                Key=key,
            )

            async with response["Body"] as stream:
                return await stream.read()

        except ClientError as e:
            logger.error(f"Error downloading file: {e}")
            raise

    async def upload_file(self, full_key: str, data: bytes, content_type: str | None = None) -> bool:
        if content_type is None:
            content_type = "text/plain"

        key = full_key.removeprefix(self._s3_bucket_name)

        try:
            await self._s3_client.put_object(
                Bucket=self._s3_bucket_name,
                Key=key,
                Body=data,
                ContentType=content_type,
            )
            return True
        except ClientError as e:
            logger.error(f"Error uploading file: {e}")
            return False

    async def delete_file(self, full_key: str) -> bool:
        key = full_key.removeprefix(self._s3_bucket_name)

        try:
            await self._s3_client.delete_object(Bucket=self._s3_bucket_name, Key=key)
            return True
        except ClientError as e:
            logger.error(f"Error deleting file: {e}")
            return False

    async def is_file_exists(self, full_key: str) -> bool:
        key = full_key.removeprefix(self._s3_bucket_name)

        try:
            await self._s3_client.head_object(Bucket=self._s3_bucket_name, Key=key)
            return True
        except ClientError as e:
            logger.error(f"Error checking file existence: {e}")
            return False


@asynccontextmanager
async def s3_storage_context() -> AsyncIterator[S3Storage]:
    async with s3_client_context() as s3_client:
        yield S3Storage(s3_client=s3_client)
