from pydantic import BaseModel
from typing import List

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    quantity: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True  # This allows returning SQLAlchemy models as responses

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    total_price: float
    user_id: int

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    user: User

    class Config:
        orm_mode = True
class CartItemBase(BaseModel):
    user_id: int
    product_id: int
    quantity: int

class CartItemCreate(CartItemBase):
    pass

class CartItem(CartItemBase):
    id: int
    class Config:
        orm_mode = True

class SaleItemBase(BaseModel):
    product_id: int
    quantity: int

class SaleCreate(BaseModel):
    user_id: int
    total_price: float
    items: List[SaleItemBase]

class Sale(SaleCreate):
    id: int
    class Config:
        orm_mode = True