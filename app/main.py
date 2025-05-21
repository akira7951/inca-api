from fastapi import FastAPI,status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.routers import files
from app.core.config import PROJECT_NAME,ALLOWED_HOST
import warnings

warnings.filterwarnings('ignore',category=FutureWarning)

app = FastAPI(title=PROJECT_NAME)
app.add_middleware( 
    CORSMiddleware,
    allow_origins=ALLOWED_HOST or ['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.api_route('/',methods=['GET'],include_in_schema=False)
async def root():
    return JSONResponse(status_code=status.HTTP_200_OK,content={'detail': 'success'})

app.include_router(files.router,prefix='/file',tags=['Files'])