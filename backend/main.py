from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import models, schemas
from models.database import SessionLocal, engine

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to My Duka API"}

# Product Routes
@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/", response_model=List[schemas.Product])
def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = db.query(models.Product).offset(skip).limit(limit).all()
    return products

# User Routes
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = user.password  # Implement password hashing here
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Order Routes
@app.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = models.Order(user_id=order.user_id, total_price=order.total_price)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/orders/{order_id}", response_model=schemas.Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

# Cart Routes
@app.post("/cart/", response_model=schemas.CartItem)
def add_to_cart(cart_item: schemas.CartItemCreate, db: Session = Depends(get_db)):
    db_cart_item = models.CartItem(**cart_item.dict())
    db.add(db_cart_item)
    db.commit()
    db.refresh(db_cart_item)
    return db_cart_item

@app.get("/cart/{user_id}", response_model=List[schemas.CartItem])
def get_cart(user_id: int, db: Session = Depends(get_db)):
    cart_items = db.query(models.CartItem).filter(models.CartItem.user_id == user_id).all()
    if not cart_items:
        raise HTTPException(status_code=404, detail="Cart is empty")
    return cart_items

@app.delete("/cart/{item_id}", response_model=schemas.CartItem)
def remove_from_cart(item_id: int, db: Session = Depends(get_db)):
    db_cart_item = db.query(models.CartItem).filter(models.CartItem.id == item_id).first()
    if not db_cart_item:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    db.delete(db_cart_item)
    db.commit()
    return db_cart_item

# Sales Routes
@app.post("/sales/", response_model=schemas.Sale)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    db_sale = models.Sale(**sale.dict())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    
    # Add SaleItems
    for item in sale.items:
        db_sale_item = models.SaleItem(sale_id=db_sale.id, product_id=item.product_id, quantity=item.quantity)
        db.add(db_sale_item)
    db.commit()
    return db_sale

@app.get("/sales/{sale_id}", response_model=schemas.Sale)
def get_sale(sale_id: int, db: Session = Depends(get_db)):
    db_sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()
    if not db_sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return db_sale
