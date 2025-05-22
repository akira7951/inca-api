from fastapi import APIRouter,File,Path,Query,UploadFile

from app.adapters.storage import create_storage_client
from app.services import file as file_sv
from typing import Optional

router = APIRouter()

@router.get('/bucketlist',name='file:bucket_list')
async def bucket_list():
    """
    Retrieve a list of all storage buckets.

    Returns:
        list: A list containing the names of all existing buckets.
    """
    storage_client = create_storage_client()
    return await file_sv.bucket_list(storage_client=storage_client)

@router.post('/create_bucket',name='file:create_bucket')
async def create_bucket(
    bucket_name: str = Query(...,description='Bucket name'),
):
    """
    Create a new storage bucket.

    Args:
        bucket_name (str): The name of the bucket to be created.

    Returns:
        dict: The result of the bucket creation operation.
    """
    storage_client = create_storage_client()
    return await file_sv.create_bucket(bucket_name,storage_client=storage_client)

@router.delete('/delete_bucket',name='file:delete_bucket')
async def delete_bucket(
    bucket_name: str = Query(...,description='Bucket name'),
):
    """
    Delete an existing storage bucket.

    Args:
        bucket_name (str): The name of the bucket to be deleted.

    Returns:
        dict: The result of the bucket deletion operation.
    """
    storage_client = create_storage_client()
    return await file_sv.delete_bucket(bucket_name,storage_client=storage_client)

@router.get('/listfiles',name='file:list')
async def list_files(
    purpose: Optional[str] = Query('assistants',description='Purpose of the file'),
    limit: Optional[int] = Query(1000,description='Limit of the file'),
    order: Optional[str] = Query('asc',description='Order of the file'),
    after: Optional[str] = Query('',description='After object name'),
):
    """"Returns a list of files"""
    storage_client = create_storage_client()
    return await file_sv.list_files(purpose,limit,order,after,storage_client=storage_client
)

@router.post('/uploadfile',name='file:upload_file')
async def upload_file(
    file: UploadFile = File(
        ...,description='The File object (not file name) to be uploaded'
    ),
    purpose: Optional[str] = Query(
        'assistants',
        description='The intended purpose of the uploaded file'
    )
):
    """"Upload a file that can be used across various endpoints"""
    
    size = file.size
    file_name = file.filename
    file_type = file.content_type
    
    storage_client = create_storage_client()
    return await file_sv.upload_file(file,purpose,size,file_name,file_type,storage_client=storage_client)

@router.delete('/deletefile/{file_id}',name='file:delete_file')
async def delete_file(
    file_id: str = Path(...,description='The ID the file to use for this request')
):
    """"Delete a file"""
    
    storage_client = create_storage_client()
    return await file_sv.delete_file(file_id,storage_client=storage_client)

@router.get('/fileinfo/{file_id}',name='file:file_info')
async def file_info(
    file_id: str = Path(...,description='The ID the file to use for this request')
):
    """"Return information about a specific file"""
    
    storage_client = create_storage_client()
    return await file_sv.file_info(file_id,storage_client=storage_client)

@router.get('/content/{file_id}',name='file:download_file')
async def file_content(
    file_id: str = Path(...,description='The ID the file to use for this request')
):
    """"Returns the content of the specific file"""
    
    storage_client = create_storage_client()
    return await file_sv.get_file_content(file_id,storage_client=storage_client)

@router.post('/copyfile/{file_id}',name='file:copy_file')
async def copy_file(
    file_id: str = Path(...,description='The ID the file to use for this request')
):
    """"Copy a file"""
    
    storage_client = create_storage_client()
    return await file_sv.copy_file(file_id,storage_client=storage_client)