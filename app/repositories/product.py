# app/repositories/product.py

from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.product import Product


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_active(self) -> List[Product]:
        stmt = select(Product).where(Product.is_active.is_(True))
        return self.db.scalars(stmt).all()

    def get_by_id(self, product_id: int) -> Optional[Product]:
        stmt = select(Product).where(Product.id == product_id)
        return self.db.scalars(stmt).one_or_none()

    def get_by_name(self, name: str) -> Optional[Product]:
        stmt = select(Product).where(func.lower(Product.name) == name.lower())
        return self.db.scalars(stmt).one_or_none()

    def create(self, product: Product) -> Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update(self, product: Product) -> Product:
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product: Product):
        self.db.delete(product)
        self.db.commit()
