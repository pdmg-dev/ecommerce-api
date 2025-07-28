# app/api/product.py

from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_product_service, require_admin
from app.models.user import User
from app.schemas.product import (ProductCreate, ProductPublicRead, ProductRead,
                                 ProductUpdate)
from app.services.product import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=list[ProductPublicRead], status_code=status.HTTP_200_OK)
def list_products(product_service: ProductService = Depends(get_product_service)):
    return product_service.list_products()


@router.get("/{product_id}", response_model=ProductRead, status_code=status.HTTP_200_OK)
def get_product(
    product_id: int, product_service: ProductService = Depends(get_product_service)
):
    return product_service.get_product(product_id)


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    create_data: ProductCreate,
    product_service: ProductService = Depends(get_product_service),
    current_user: User = Depends(require_admin),
):
    return product_service.create_product(create_data)


@router.patch(
    "/{product_id}", response_model=ProductRead, status_code=status.HTTP_200_OK
)
def update_product(
    product_id: int,
    update_data: ProductUpdate,
    product_service: ProductService = Depends(get_product_service),
    current_user: User = Depends(require_admin),
):
    return product_service.update_product(product_id, update_data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    product_service: ProductService = Depends(get_product_service),
    current_user: User = Depends(require_admin),
):
    product_service.delete_product(product_id)
