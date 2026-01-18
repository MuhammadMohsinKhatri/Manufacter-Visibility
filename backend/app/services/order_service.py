from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from app.models.models import Order, OrderItem, Product, Component, ProductComponent, InventoryItem, ProductionLine, ProductionSchedule
from app.schemas.order import OrderCreate, OrderUpdate, OrderFeasibilityCheck
from app.services.inventory_service import check_component_availability
from app.services.production_service import check_production_capacity
from app.services.risk_service import assess_supply_chain_risks

class OrderService:
    @staticmethod
    def create_order(db: Session, order_data: OrderCreate) -> Order:
        """Create a new order with order items"""
        # Create order
        db_order = Order(
            customer_id=order_data.customer_id,
            notes=order_data.notes,
            estimated_delivery=order_data.estimated_delivery
        )
        db.add(db_order)
        db.flush()  # Flush to get the order ID
        
        # Create order items
        for item in order_data.items:
            db_item = OrderItem(
                order_id=db_order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price
            )
            db.add(db_item)
        
        db.commit()
        db.refresh(db_order)
        return db_order
    
    @staticmethod
    def update_order(db: Session, order_id: int, order_data: OrderUpdate) -> Optional[Order]:
        """Update an existing order"""
        db_order = db.query(Order).filter(Order.id == order_id).first()
        if not db_order:
            return None
        
        # Update order fields if provided
        if order_data.status is not None:
            db_order.status = order_data.status
        if order_data.estimated_delivery is not None:
            db_order.estimated_delivery = order_data.estimated_delivery
        if order_data.actual_delivery is not None:
            db_order.actual_delivery = order_data.actual_delivery
        if order_data.notes is not None:
            db_order.notes = order_data.notes
        
        db.commit()
        db.refresh(db_order)
        return db_order
    
    @staticmethod
    def get_order(db: Session, order_id: int) -> Optional[Order]:
        """Get an order by ID"""
        return db.query(Order).filter(Order.id == order_id).first()
    
    @staticmethod
    def get_orders(db: Session, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get all orders with pagination"""
        return db.query(Order).offset(skip).limit(limit).all()
    
    @staticmethod
    def delete_order(db: Session, order_id: int) -> bool:
        """Delete an order by ID"""
        db_order = db.query(Order).filter(Order.id == order_id).first()
        if not db_order:
            return False
        
        db.delete(db_order)
        db.commit()
        return True
    
    @staticmethod
    def check_order_feasibility(
        db: Session, 
        feasibility_check: OrderFeasibilityCheck
    ) -> Dict[str, Any]:
        """
        Check if an order is feasible based on inventory and production capacity
        Returns feasibility information including earliest possible delivery date
        """
        result = {
            "feasible": False,
            "earliest_possible_date": None,
            "inventory_constraints": [],
            "production_constraints": [],
            "risk_factors": [],
            "confidence_score": 0.0
        }
        
        # Get products and their required components
        products_with_components = []
        for i, product_id in enumerate(feasibility_check.product_ids):
            quantity = feasibility_check.quantities[i]
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                result["inventory_constraints"].append(f"Product ID {product_id} not found")
                continue
                
            # Get all components required for this product
            components = db.query(
                Component, ProductComponent.quantity_required
            ).join(
                ProductComponent, ProductComponent.component_id == Component.id
            ).filter(
                ProductComponent.product_id == product_id
            ).all()
            
            products_with_components.append({
                "product": product,
                "quantity": quantity,
                "components": [(comp, qty * quantity) for comp, qty in components]
            })
        
        # Check component availability
        all_components_available = True
        for product_info in products_with_components:
            for component, required_qty in product_info["components"]:
                availability = check_component_availability(db, component.id, required_qty)
                if not availability["available"]:
                    all_components_available = False
                    result["inventory_constraints"].append(
                        f"Insufficient {component.name}: need {required_qty}, have {availability['available_quantity']}"
                    )
        
        # Check production capacity
        requested_date = feasibility_check.requested_delivery_date or (datetime.utcnow() + timedelta(days=14))
        production_capacity = check_production_capacity(
            db, 
            datetime.utcnow(),  # Start from now
            requested_date      # Until requested date
        )
        
        # Calculate total production time needed
        total_production_hours = 0
        for product_info in products_with_components:
            # Simplified calculation - in real system would be more complex
            # based on product complexity, setup time, etc.
            total_production_hours += product_info["quantity"] * 2  # Assume 2 hours per unit
        
        if production_capacity["available_hours"] < total_production_hours:
            result["production_constraints"].append(
                f"Insufficient production capacity: need {total_production_hours} hours, " +
                f"have {production_capacity['available_hours']} hours available"
            )
            
            # Calculate earliest possible date based on production constraints
            extra_days_needed = ((total_production_hours - production_capacity["available_hours"]) / 24) + 1
            earliest_date_production = requested_date + timedelta(days=int(extra_days_needed))
        else:
            earliest_date_production = requested_date
        
        # Check supply chain risks
        risk_assessment = assess_supply_chain_risks(
            db,
            component_ids=[comp.id for product_info in products_with_components 
                          for comp, _ in product_info["components"]],
            time_horizon_days=30
        )
        
        if risk_assessment["overall_risk_score"] > 50:  # Threshold for high risk
            result["risk_factors"] = [
                f"{risk.risk_type} risk in {risk.region}: {risk.description}" 
                for risk in risk_assessment["risks"][:3]  # Top 3 risks
            ]
            
            # Adjust earliest date based on risk factors
            risk_delay_days = int(risk_assessment["overall_risk_score"] / 20)  # Simple formula
            earliest_date_with_risks = earliest_date_production + timedelta(days=risk_delay_days)
        else:
            earliest_date_with_risks = earliest_date_production
        
        # Determine final feasibility
        result["earliest_possible_date"] = earliest_date_with_risks
        result["feasible"] = (
            all_components_available and 
            production_capacity["available_hours"] >= total_production_hours and
            risk_assessment["overall_risk_score"] < 70  # Very high risk threshold
        )
        
        # Calculate confidence score
        inventory_confidence = 100 if all_components_available else 50
        production_confidence = min(100, (production_capacity["available_hours"] / total_production_hours) * 100) if total_production_hours > 0 else 100
        risk_confidence = max(0, 100 - risk_assessment["overall_risk_score"])
        
        result["confidence_score"] = (inventory_confidence * 0.4 + production_confidence * 0.4 + risk_confidence * 0.2)
        
        return result