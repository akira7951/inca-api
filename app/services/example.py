from fastapi import status
from fastapi.responses import JSONResponse

def example():
    resp = {'detail': 'success'}
    return JSONResponse(status_code=status.HTTP_200_OK,content=resp)