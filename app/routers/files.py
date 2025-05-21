from fastapi import APIRouter,File,Path,Query,UploadFile

from app.adapters.storage import create_storage_client
from app.services import file as file_sv
from typing import Optional

router = APIRouter()

@router.get('/bucketlist',name='file:bucket_list')
async def bucket_list():
    storage_client = create_storage_client()
    return await file_sv.bucket_list(storage_client=storage_client)