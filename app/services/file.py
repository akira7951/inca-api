from fastapi import UploadFile,status
from fastapi.responses import JSONResponse

from app.adapters.storage import create_storage_client,StorageClient

FILE_BUCKET_NAME: str = 'raw-files'
storageClient = create_storage_client()

async def bucket_list(storage_client: StorageClient)->JSONResponse:
    """Get bucket list"""
    get_list = storage_client.list_buckets()
    
    data = [
        {
            'name': b.name,
            'creation_date': b.creation_date.isoformat(),
        }
        for b in get_list
    ]
    
    resp = {'object': 'list','data': data}
    return JSONResponse(status_code=status.HTTP_200_OK,content=resp)

async def create_bucket(bucket_name: str,storage_client: StorageClient)->JSONResponse:
    """Create bucket"""
    try:
        storage_client.make_bucket(bucket_name)
        resp = {'object': 'bucket','data': bucket_name}
        return JSONResponse(status_code=status.HTTP_201_CREATED,content=resp)
    except Exception as e:
        resp = {'object': 'bucket','data': str(e)}
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content=resp)