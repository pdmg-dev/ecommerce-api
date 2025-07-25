# app/api/product.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_admin
from app.db.deps import get_db
from app.models.user import User
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services.product import ProductService

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=list[ProductRead])
def list_products(db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.list_products()

@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.get_product(product_id)

@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    # NOTE: Add is_admin check later
    service = ProductService(db)
    return service.create_product(product_in)

@router.patch("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    # NOTE: Add is_admin check later
    service = ProductService(db)
    return service.update_product(product_id, product_in)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    # NOTE: Add is_admin check later
    service = ProductService(db)
    service.delete_product(product_id)