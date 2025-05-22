from fastapi import UploadFile,status
from fastapi.responses import JSONResponse,StreamingResponse
from minio.commonconfig import CopySource

from app.adapters.storage import create_storage_client,StorageClient
from zoneinfo import ZoneInfo
from datetime import datetime
import uuid,io

FILE_BUCKET_NAME: str = 'raw-file'
storageClient = create_storage_client()

async def bucket_list(storage_client: StorageClient)->JSONResponse:
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
    try:
        storage_client.make_bucket(bucket_name)
        resp = {'object': 'bucket','data': bucket_name}
        return JSONResponse(status_code=status.HTTP_201_CREATED,content=resp)
    except Exception as e:
        resp = {'object': 'bucket','data': str(e)}
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content=resp)

async def delete_bucket(bucket_name: str,storage_client: StorageClient)->JSONResponse:
    try:
        storage_client.remove_bucket(bucket_name)
        resp = {'object': 'bucket','data': bucket_name}
        return JSONResponse(status_code=status.HTTP_200_OK,content=resp)
    except Exception as e:
        resp = {'object': 'bucket','data': str(e)}
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content=resp)

async def list_files(purpose: str,limit: int,order: str,after: str,storage_client: StorageClient)->JSONResponse:
    objects = storage_client.list_objects(
        FILE_BUCKET_NAME,start_after=after,recursive=True
    )
    
    object_list = []
    for obj in objects:
        metadata = storage_client.stat_object(FILE_BUCKET_NAME,obj.object_name)
        obj_purpose = metadata.metadata.get('X-Amz-Meta-Purpose','assistants')
        if obj_purpose != purpose:
            continue
        
        filename = metadata.metadata.get('X-Amz-Meta-Filename')
        if not filename:
            filename = obj.object_name
        
        created_at = obj.last_modified.astimezone(ZoneInfo('Asia/Taipei')).strftime('%Y-%m-%d %H:%M:%S')
        
        object_info = {
            'id': obj.object_name,
            'bytes': obj.size,
            'created_at': created_at,
            'expires_at': None,
            'filema,e': filename,
            'purpose': obj_purpose,
        }
        object_list.append(object_info)
        
        if len(object_list) >= limit:
            break
    
    reverse = True if order == 'desc' else False
    object_list.sort(key=lambda x: x['created_at'],reverse=reverse)
    
    first_id = object_list[0]['id'] if object_list else None
    last_id = object_list[-1]['id'] if object_list else None
    has_more = len(object_list) >= limit
    
    resp = {
        'object': 'list',
        'data': object_list,
        'first_id': first_id,
        'last_id': last_id,
        'has_more': has_more,
    }
    return JSONResponse(status_code=status.HTTP_200_OK,content=resp)

async def upload_file(file: UploadFile,purpose: str,size: int,file_name: str,file_type: str,storage_client: StorageClient)->JSONResponse:
    file_id = str(uuid.uuid4())
    
    try:
        content = await file.read()
        file_data = io.BytesIO(content)
        
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        storage_client.put_object(
            FILE_BUCKET_NAME,
            file_id,
            data=file_data,
            length=size,
            metadata={
                'purpose': str(purpose),
                'filename': file_name if file_name else file_id
            },
            content_type=file_type
        )
        
        resp = {
            'id': file_id,
            'object': 'file',
            'bytes': size,
            'created_at': created_at,
            'expired_at': None,
            'file_name': file_name,
            'purpose': purpose
        }
        return JSONResponse(status_code=status.HTTP_200_OK,content=resp)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'error': f"Unexpcted error: {str(e)}"}
        )

async def delete_file(file_id: uuid.UUID,storage_client: StorageClient)->JSONResponse:
    storage_client.remove_object(FILE_BUCKET_NAME,file_id)
    
    resp = {
        'id': str(file_id),
        'object': 'file',
        'delete': True
    }
    return JSONResponse(status_code=status.HTTP_200_OK,content=resp)

async def file_info(file_id: uuid.UUID,storage_client: StorageClient)->JSONResponse:
    try:
        object_stat = storage_client.stat_object(FILE_BUCKET_NAME,str(file_id))
        created_at = object_stat.last_modified.astimezone(
            ZoneInfo('Asia/Taipei')
        ).strftime('%Y-%m-%d %H:%M:%S')
        
        metadata = object_stat.metadata
        purpose = metadata.get('X-Amz-Meta-Purpose')
        filename = metadata.get('X-Amz-Meta-Filename')
        file_size = object_stat.size
        
        resp = {
            'id': str(file_id),
            'bytes': file_size,
            'created_at': created_at,
            'expired_at': None,
            'filename': filename,
            'object': 'file',
            'purpose': purpose
        }
        return JSONResponse(status_code=status.HTTP_200_OK,content=resp)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'error': f"Unexpcted error: {str(e)}"}
        )

async def get_file_content(file_id: uuid.UUID,storage_client: StorageClient):
    object_stat = storage_client.stat_object(FILE_BUCKET_NAME,str(file_id))
    metadata = object_stat.metadata
    filename = metadata.get('X-Amz-Meta-Filename')
    response = storage_client.get_object(FILE_BUCKET_NAME,str(file_id))
    
    return StreamingResponse(
        response.stream(32*1024),
        media_type='application/octet-stream',
        headers={'Content-Disposition': f"attachment; filename={filename}"}
    )

async def copy_file(source_file_id: uuid.UUID,storage_client: StorageClient)->JSONResponse:
    new_file_id = str(uuid.uuid4())
    
    try:
        object_stat = storage_client.stat_object(FILE_BUCKET_NAME,source_file_id)
        metadata = object_stat.metadata
        purpose = metadata.get('X-Amz-Meta-Purpose')
        filename = metadata.get('X-Amz-Meta-Filename')
        
        source = CopySource(FILE_BUCKET_NAME,source_file_id)
        
        new_metadata = {
            'purpose': purpose,
            'filename': filename,
            'copy_from': source_file_id
        }
        
        storage_client.copy_object(
            FILE_BUCKET_NAME,new_file_id,source,
            metadata=new_metadata,
            metadata_directive='REPLACE'
        )
        
        resp = {'detail': f'Object copied with metadata. New object: {new_file_id}'}
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={'error': f"Unexpcted error: {str(e)}"}
        )
