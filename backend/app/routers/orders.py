from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.models.models import Order
from app.schemas.order import (
    OrderCreate, OrderResponse, OrderUpdate,
    OrderFeasibilityCheck, OrderFeasibilityResponse
)
from app.services.order_service import OrderService

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """Create a new order"""
    return OrderService.create_order(db, order)

@router.get("/", response_model=List[OrderResponse])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all orders"""
    return OrderService.get_orders(db, skip=skip, limit=limit)

@router.get("/{order_id}", response_model=OrderResponse)
def read_order(order_id: int, db: Session = Depends(get_db)):
    """Get an order by ID"""
    db_order = OrderService.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.put("/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    """Update an order"""
    db_order = OrderService.update_order(db, order_id=order_id, order_data=order)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """Delete an order"""
    success = OrderService.delete_order(db, order_id=order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}

@router.post("/check-feasibility", response_model=OrderFeasibilityResponse)
def check_order_feasibility(check: OrderFeasibilityCheck, db: Session = Depends(get_db)):
    """Check if an order is feasible based on inventory and production capacity"""
    result = OrderService.check_order_feasibility(db, check)
    return result