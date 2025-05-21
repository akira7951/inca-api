from typing import TypeAlias
from minio import Minio
from app.core.config import MINIO_HOST,MINIO_ACCESS_KEY,MINIO_SECRET_KEY

StorageClient: TypeAlias = Minio

def create_storage_client()->StorageClient:
    """Factory of client store"""
    
    client = Minio(
        MINIO_HOST,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False
    )
    return client