from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.models.models import Component, InventoryItem, ProductComponent, Product

def get_component(db: Session, component_id: int) -> Optional[Component]:
    """Get a component by ID"""
    return db.query(Component).filter(Component.id == component_id).first()

def get_components(db: Session, skip: int = 0, limit: int = 100) -> List[Component]:
    """Get all components with pagination"""
    return db.query(Component).offset(skip).limit(limit).all()

def create_component(db: Session, name: str, description: str, sku: str) -> Component:
    """Create a new component"""
    db_component = Component(name=name, description=description, sku=sku)
    db.add(db_component)
    db.commit()
    db.refresh(db_component)
    return db_component

def get_inventory_item(db: Session, inventory_id: int) -> Optional[InventoryItem]:
    """Get an inventory item by ID"""
    return db.query(InventoryItem).filter(InventoryItem.id == inventory_id).first()

def get_inventory_by_component(db: Session, component_id: int) -> Optional[InventoryItem]:
    """Get inventory item for a specific component"""
    return db.query(InventoryItem).filter(InventoryItem.component_id == component_id).first()

def get_all_inventory(db: Session, skip: int = 0, limit: int = 100) -> List[InventoryItem]:
    """Get all inventory items with pagination"""
    return db.query(InventoryItem).offset(skip).limit(limit).all()

def create_inventory_item(
    db: Session, 
    component_id: int, 
    quantity_available: int,
    reorder_threshold: int = 10,
    location: str = None
) -> InventoryItem:
    """Create a new inventory item"""
    db_inventory = InventoryItem(
        component_id=component_id,
        quantity_available=quantity_available,
        quantity_allocated=0,
        reorder_threshold=reorder_threshold,
        location=location
    )
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

def update_inventory_quantity(
    db: Session, 
    inventory_id: int, 
    quantity_change: int
) -> Optional[InventoryItem]:
    """Update inventory quantity (positive for addition, negative for removal)"""
    db_inventory = db.query(InventoryItem).filter(InventoryItem.id == inventory_id).first()
    if not db_inventory:
        return None
    
    db_inventory.quantity_available += quantity_change
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

def allocate_inventory(
    db: Session, 
    component_id: int, 
    quantity: int
) -> Dict[str, Any]:
    """Allocate inventory for a component"""
    db_inventory = db.query(InventoryItem).filter(InventoryItem.component_id == component_id).first()
    if not db_inventory:
        return {
            "success": False,
            "message": f"No inventory found for component ID {component_id}",
            "allocated_quantity": 0,
            "remaining_quantity": 0
        }
    
    available = db_inventory.quantity_available - db_inventory.quantity_allocated
    
    if available < quantity:
        return {
            "success": False,
            "message": f"Insufficient inventory. Requested: {quantity}, Available: {available}",
            "allocated_quantity": 0,
            "remaining_quantity": available
        }
    
    db_inventory.quantity_allocated += quantity
    db.commit()
    
    return {
        "success": True,
        "message": f"Successfully allocated {quantity} units",
        "allocated_quantity": quantity,
        "remaining_quantity": db_inventory.quantity_available - db_inventory.quantity_allocated
    }

def check_component_availability(
    db: Session, 
    component_id: int, 
    required_quantity: int
) -> Dict[str, Any]:
    """Check if a component is available in sufficient quantity"""
    db_inventory = db.query(InventoryItem).filter(InventoryItem.component_id == component_id).first()
    
    if not db_inventory:
        return {
            "available": False,
            "component_id": component_id,
            "required_quantity": required_quantity,
            "available_quantity": 0,
            "message": "Component not found in inventory"
        }
    
    available = db_inventory.quantity_available - db_inventory.quantity_allocated
    
    return {
        "available": available >= required_quantity,
        "component_id": component_id,
        "required_quantity": required_quantity,
        "available_quantity": available,
        "message": "Sufficient inventory" if available >= required_quantity else "Insufficient inventory"
    }

def check_product_components_availability(
    db: Session, 
    product_id: int, 
    quantity: int
) -> Dict[str, Any]:
    """Check availability of all components needed for a product"""
    # Get all components required for this product
    components = db.query(
        Component, ProductComponent.quantity_required
    ).join(
        ProductComponent, ProductComponent.component_id == Component.id
    ).filter(
        ProductComponent.product_id == product_id
    ).all()
    
    if not components:
        return {
            "available": False,
            "product_id": product_id,
            "message": "No components found for this product",
            "component_availability": []
        }
    
    component_availability = []
    all_available = True
    
    for component, required_qty in components:
        # Calculate total required quantity
        total_required = required_qty * quantity
        
        # Check availability
        availability = check_component_availability(db, component.id, total_required)
        component_availability.append(availability)
        
        if not availability["available"]:
            all_available = False
    
    return {
        "available": all_available,
        "product_id": product_id,
        "message": "All components available" if all_available else "Some components unavailable",
        "component_availability": component_availability
    }

def get_low_stock_items(db: Session) -> List[Dict[str, Any]]:
    """Get items that are below their reorder threshold"""
    low_stock_items = []
    
    inventory_items = db.query(InventoryItem).all()
    for item in inventory_items:
        if item.quantity_available <= item.reorder_threshold:
            component = db.query(Component).filter(Component.id == item.component_id).first()
            low_stock_items.append({
                "inventory_id": item.id,
                "component_id": item.component_id,
                "component_name": component.name if component else "Unknown",
                "sku": component.sku if component else "Unknown",
                "quantity_available": item.quantity_available,
                "reorder_threshold": item.reorder_threshold,
                "shortage": item.reorder_threshold - item.quantity_available
            })
    
    return low_stock_items