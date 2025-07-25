# app/services/product.py

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.product import Product
from app.repositories.product import ProductRepository
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate


class ProductService:
    def __init__(self, db: Session):
        self.repo = ProductRepository(db)

    def list_products(self) -> list[ProductRead]:
        products = self.repo.get_all()
        return [ProductRead.model_validate(p) for p in products]

    def get_product(self, product_id: int) -> ProductRead:
        product = self.repo.get_by_id(product_id)
        if not product or not product.is_active:
            raise HTTPException(status_code=404, detail="Product not found")
        return ProductRead.model_validate(product)

    def create_product(self, data: ProductCreate) -> ProductRead:
        product = self.repo.create(data)
        return ProductRead.model_validate(product)

    def update_product(self, product_id: int, data: ProductUpdate) -> ProductRead:
        product = self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        updated = self.repo.update(product, data)
        return ProductRead.model_validate(updated)

    def delete_product(self, product_id: int):
        product = self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        self.repo.delete(product)
