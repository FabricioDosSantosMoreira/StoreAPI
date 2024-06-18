from fastapi import APIRouter, Body, Depends, status

from store.usecases.product import ProductUsecase
from store.schemas.product import ProductIn, ProductOut


router = APIRouter(tags=["products"])


@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def post(
    body: ProductIn = Body(...), usecase: ProductUsecase = Depends()
) -> ProductOut:
    return await usecase.create(body=body)
