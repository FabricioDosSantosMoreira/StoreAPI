
from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from pydantic import UUID4
from store.core.exception import NotFoundException, GenericException
from store.usecases.product import ProductUsecase
from store.schemas.product import ProductOut, ProductCreateIn, ProductUpdateIn

router = APIRouter(tags=["products"])


@router.post(
    path="/", 
    status_code=status.HTTP_201_CREATED,
)
async def post(
    body: ProductCreateIn = Body(...), 
    usecase: ProductUsecase = Depends(),
) -> ProductOut:
    
    try:
        return await usecase.create(body=body)
    except GenericException as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=exc.message
        )


@router.get(
    path="/{id}", 
    status_code=status.HTTP_200_OK,
)
async def get(
    id: UUID4 = Path(alias="id"), 
    usecase: ProductUsecase = Depends(),
) -> ProductOut:
    
    try:
        return await usecase.get_by_id(id=id)
    except NotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=exc.message
        )
    except GenericException as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=exc.message
        )


@router.get(
    path="/", 
    status_code=status.HTTP_200_OK,
)
async def get(
    usecase: ProductUsecase = Depends(),
)-> List[ProductOut]:
    
    try:
        return await usecase.get_all()
    except NotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=exc.message
        )
    except GenericException as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=exc.message
        )
    

@router.patch(
    path="/{id}", 
    status_code=status.HTTP_200_OK,
)
async def patch(
    id: UUID4 = Path(alias="id"),
    body: ProductUpdateIn = Body(...),
    usecase: ProductUsecase = Depends(),
) -> ProductOut:
    
    try:
        return await usecase.update(id=id, body=body)
    except NotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=exc.message
        )
    except GenericException as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=exc.message
        )


@router.delete(
    path="/{id}", 
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    id: UUID4 = Path(alias="id"), 
    usecase: ProductUsecase = Depends(),
) -> None:
    
    try:
        await usecase.delete(id=id)
    except NotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=exc.message
        )
    except GenericException as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=exc.message
        )
    
