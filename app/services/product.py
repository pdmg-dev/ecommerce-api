# app/services/product.py

from app.models.product import Product
from app.repositories.product import ProductRepository
from app.schemas.product import (
    ProductCreate,
    ProductPublicRead,
    ProductRead,
    ProductUpdate,
)
from app.utils import exceptions


class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def list_products(self) -> list[ProductPublicRead]:
        products = self.product_repository.get_all_active()
        return [ProductPublicRead.model_validate(p) for p in products]

    def get_product(self, product_id: int) -> ProductRead:
        product = self.product_repository.get_by_id(product_id)
        if not product or not product.is_active:
            raise exceptions.not_found("Product not found")
        return ProductRead.model_validate(product)

    def create_product(self, create_data: ProductCreate) -> ProductRead:
        existing_product = self.product_repository.get_by_name(create_data.name)
        if existing_product:
            raise exceptions.bad_request("Product already exists")

        new_product = Product(**create_data.model_dump())

        saved_product = self.product_repository.create(new_product)
        return ProductRead.model_validate(saved_product)

    def update_product(
        self, product_id: int, update_data: ProductUpdate
    ) -> ProductRead:
        product = self.product_repository.get_by_id(product_id)
        if not product or not product.is_active:
            raise exceptions.not_found("Product not found or inactive")

        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(product, field, value)

        updated_product = self.product_repository.update(product)
        return ProductRead.model_validate(updated_product)

    def delete_product(self, product_id: int):
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise exceptions.not_found("Product not found or inactive")
        self.product_repository.delete(product)
