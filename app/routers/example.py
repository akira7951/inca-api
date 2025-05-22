from fastapi import APIRouter
from app.services import example as exp

router = APIRouter()

@router.get('/t1',name='example',include_in_schema=False)
async def example_t1():
    return exp.example()