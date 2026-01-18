from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.schemas.inventory import (
    ComponentCreate, ComponentResponse,
    InventoryItemCreate, InventoryItemResponse, InventoryItemUpdate,
    InventoryAllocationRequest, InventoryAllocationResponse
)
from app.services.inventory_service import (
    get_component, get_components, create_component,
    get_inventory_item, get_inventory_by_component, get_all_inventory,
    create_inventory_item, update_inventory_quantity, allocate_inventory,
    check_component_availability, check_product_components_availability,
    get_low_stock_items
)

router = APIRouter(
    prefix="/inventory",
    tags=["inventory"],
    responses={404: {"description": "Not found"}},
)

# Component routes
@router.post("/components/", response_model=ComponentResponse, status_code=status.HTTP_201_CREATED)
def create_new_component(component: ComponentCreate, db: Session = Depends(get_db)):
    """Create a new component"""
    return create_component(db, component.name, component.description, component.sku)

@router.get("/components/", response_model=List[ComponentResponse])
def read_components(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all components"""
    return get_components(db, skip=skip, limit=limit)

@router.get("/components/{component_id}", response_model=ComponentResponse)
def read_component(component_id: int, db: Session = Depends(get_db)):
    """Get a component by ID"""
    db_component = get_component(db, component_id=component_id)
    if db_component is None:
        raise HTTPException(status_code=404, detail="Component not found")
    return db_component

# Inventory routes
@router.post("/items/", response_model=InventoryItemResponse, status_code=status.HTTP_201_CREATED)
def create_new_inventory_item(inventory: InventoryItemCreate, db: Session = Depends(get_db)):
    """Create a new inventory item"""
    # Check if component exists
    component = get_component(db, component_id=inventory.component_id)
    if component is None:
        raise HTTPException(status_code=404, detail="Component not found")
    
    # Check if inventory already exists for this component
    existing_inventory = get_inventory_by_component(db, component_id=inventory.component_id)
    if existing_inventory:
        raise HTTPException(status_code=400, detail="Inventory already exists for this component")
    
    return create_inventory_item(
        db, 
        inventory.component_id, 
        inventory.quantity_available,
        inventory.reorder_threshold,
        inventory.location
    )

@router.get("/items/", response_model=List[InventoryItemResponse])
def read_inventory_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all inventory items"""
    return get_all_inventory(db, skip=skip, limit=limit)

@router.get("/items/{inventory_id}", response_model=InventoryItemResponse)
def read_inventory_item(inventory_id: int, db: Session = Depends(get_db)):
    """Get an inventory item by ID"""
    db_inventory = get_inventory_item(db, inventory_id=inventory_id)
    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return db_inventory

@router.get("/by-component/{component_id}", response_model=InventoryItemResponse)
def read_inventory_by_component(component_id: int, db: Session = Depends(get_db)):
    """Get inventory for a specific component"""
    db_inventory = get_inventory_by_component(db, component_id=component_id)
    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found for this component")
    return db_inventory

@router.put("/items/{inventory_id}", response_model=InventoryItemResponse)
def update_inventory_item(inventory_id: int, inventory: InventoryItemUpdate, db: Session = Depends(get_db)):
    """Update an inventory item"""
    db_inventory = get_inventory_item(db, inventory_id=inventory_id)
    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    
    # Update fields if provided
    if inventory.quantity_available is not None:
        db_inventory.quantity_available = inventory.quantity_available
    if inventory.quantity_allocated is not None:
        db_inventory.quantity_allocated = inventory.quantity_allocated
    if inventory.reorder_threshold is not None:
        db_inventory.reorder_threshold = inventory.reorder_threshold
    if inventory.location is not None:
        db_inventory.location = inventory.location
    
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

@router.post("/allocate", response_model=InventoryAllocationResponse)
def allocate_component_inventory(allocation: InventoryAllocationRequest, db: Session = Depends(get_db)):
    """Allocate inventory for a component"""
    result = allocate_inventory(db, allocation.component_id, allocation.quantity)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@router.get("/check-availability/{component_id}")
def check_availability(component_id: int, quantity: int, db: Session = Depends(get_db)):
    """Check if a component is available in sufficient quantity"""
    return check_component_availability(db, component_id, quantity)

@router.get("/check-product-availability/{product_id}")
def check_product_availability(product_id: int, quantity: int, db: Session = Depends(get_db)):
    """Check availability of all components needed for a product"""
    return check_product_components_availability(db, product_id, quantity)

@router.get("/low-stock")
def get_low_stock(db: Session = Depends(get_db)):
    """Get items that are below their reorder threshold"""
    return get_low_stock_items(db)