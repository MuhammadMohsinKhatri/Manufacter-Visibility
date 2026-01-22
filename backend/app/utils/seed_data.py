import sys
import os
from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database.database import SessionLocal, engine, Base
from app.models.models import (
    Customer, Product, Component, ProductComponent, InventoryItem,
    Order, OrderItem, Supplier, SupplierComponent, ProductionLine,
    ProductionSchedule, Shipment, ShipmentItem, ExternalRisk, User,
    Staff, TaskAssignment, OrderStatus, SupplierReliability, RiskLevel
)

def seed_database():
    """Seed the database with demo data"""
    db = SessionLocal()
    try:
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        
        # Only seed if database is empty
        if db.query(Customer).count() > 0:
            print("Database already contains data. Skipping seed operation.")
            return
        
        print("Seeding database with demo data...")
        
        # Create customers
        print("Creating customers...")
        customers = [
            Customer(
                name="Acme Corporation",
                contact_person="John Smith",
                email="john.smith@acme.com",
                phone="555-123-4567",
                address="123 Main St, Anytown, USA"
            ),
            Customer(
                name="Globex Industries",
                contact_person="Jane Doe",
                email="jane.doe@globex.com",
                phone="555-987-6543",
                address="456 Oak Ave, Somewhere, USA"
            ),
            Customer(
                name="Initech Systems",
                contact_person="Michael Bolton",
                email="michael.bolton@initech.com",
                phone="555-246-8101",
                address="789 Pine Rd, Elsewhere, USA"
            ),
            Customer(
                name="Umbrella Corporation",
                contact_person="Alice Johnson",
                email="alice.johnson@umbrella.com",
                phone="555-369-1470",
                address="321 Elm St, Nowhere, USA"
            ),
            Customer(
                name="Stark Industries",
                contact_person="Tony Stark",
                email="tony.stark@stark.com",
                phone="555-789-4561",
                address="10880 Malibu Point, Malibu, USA"
            )
        ]
        db.add_all(customers)
        db.commit()
        
        # Create components
        print("Creating components...")
        components = [
            Component(name="Steel Frame", description="Main structural frame", sku="SF-001"),
            Component(name="Rubber Gasket", description="Sealing gasket", sku="RG-002"),
            Component(name="Circuit Board", description="Main control board", sku="CB-003"),
            Component(name="Power Supply", description="240V power supply", sku="PS-004"),
            Component(name="LCD Display", description="User interface display", sku="LCD-005"),
            Component(name="Aluminum Housing", description="Exterior casing", sku="AH-006"),
            Component(name="Cooling Fan", description="Internal cooling system", sku="CF-007"),
            Component(name="Wiring Harness", description="Internal wiring", sku="WH-008"),
            Component(name="Mounting Bracket", description="Installation bracket", sku="MB-009"),
            Component(name="Sensor Array", description="Environmental sensors", sku="SA-010")
        ]
        db.add_all(components)
        db.commit()
        
        # Create products
        print("Creating products...")
        products = [
            Product(
                name="Industrial Controller",
                description="Heavy duty industrial control system",
                sku="IC-100",
                price=1299.99
            ),
            Product(
                name="Smart Thermostat",
                description="IoT-enabled temperature control",
                sku="ST-200",
                price=249.99
            ),
            Product(
                name="Power Management Unit",
                description="Enterprise power distribution system",
                sku="PMU-300",
                price=3499.99
            ),
            Product(
                name="Security Gateway",
                description="Industrial security appliance",
                sku="SG-400",
                price=1899.99
            ),
            Product(
                name="Environmental Monitor",
                description="Multi-sensor monitoring system",
                sku="EM-500",
                price=899.99
            )
        ]
        db.add_all(products)
        db.commit()
        
        # Create product components (bill of materials)
        print("Creating product components (BOM)...")
        product_components = []
        
        # Industrial Controller components
        product_components.extend([
            ProductComponent(product_id=1, component_id=1, quantity_required=1),  # Steel Frame
            ProductComponent(product_id=1, component_id=2, quantity_required=4),  # Rubber Gasket
            ProductComponent(product_id=1, component_id=3, quantity_required=2),  # Circuit Board
            ProductComponent(product_id=1, component_id=4, quantity_required=1),  # Power Supply
            ProductComponent(product_id=1, component_id=6, quantity_required=1),  # Aluminum Housing
            ProductComponent(product_id=1, component_id=7, quantity_required=2),  # Cooling Fan
            ProductComponent(product_id=1, component_id=8, quantity_required=1),  # Wiring Harness
        ])
        
        # Smart Thermostat components
        product_components.extend([
            ProductComponent(product_id=2, component_id=3, quantity_required=1),  # Circuit Board
            ProductComponent(product_id=2, component_id=5, quantity_required=1),  # LCD Display
            ProductComponent(product_id=2, component_id=6, quantity_required=1),  # Aluminum Housing
            ProductComponent(product_id=2, component_id=8, quantity_required=1),  # Wiring Harness
            ProductComponent(product_id=2, component_id=10, quantity_required=3), # Sensor Array
        ])
        
        # Power Management Unit components
        product_components.extend([
            ProductComponent(product_id=3, component_id=1, quantity_required=2),  # Steel Frame
            ProductComponent(product_id=3, component_id=3, quantity_required=4),  # Circuit Board
            ProductComponent(product_id=3, component_id=4, quantity_required=3),  # Power Supply
            ProductComponent(product_id=3, component_id=6, quantity_required=1),  # Aluminum Housing
            ProductComponent(product_id=3, component_id=7, quantity_required=4),  # Cooling Fan
            ProductComponent(product_id=3, component_id=8, quantity_required=2),  # Wiring Harness
            ProductComponent(product_id=3, component_id=9, quantity_required=2),  # Mounting Bracket
        ])
        
        # Security Gateway components
        product_components.extend([
            ProductComponent(product_id=4, component_id=1, quantity_required=1),  # Steel Frame
            ProductComponent(product_id=4, component_id=3, quantity_required=3),  # Circuit Board
            ProductComponent(product_id=4, component_id=4, quantity_required=1),  # Power Supply
            ProductComponent(product_id=4, component_id=5, quantity_required=1),  # LCD Display
            ProductComponent(product_id=4, component_id=6, quantity_required=1),  # Aluminum Housing
            ProductComponent(product_id=4, component_id=7, quantity_required=2),  # Cooling Fan
            ProductComponent(product_id=4, component_id=8, quantity_required=1),  # Wiring Harness
        ])
        
        # Environmental Monitor components
        product_components.extend([
            ProductComponent(product_id=5, component_id=3, quantity_required=1),  # Circuit Board
            ProductComponent(product_id=5, component_id=4, quantity_required=1),  # Power Supply
            ProductComponent(product_id=5, component_id=5, quantity_required=1),  # LCD Display
            ProductComponent(product_id=5, component_id=6, quantity_required=1),  # Aluminum Housing
            ProductComponent(product_id=5, component_id=8, quantity_required=1),  # Wiring Harness
            ProductComponent(product_id=5, component_id=9, quantity_required=1),  # Mounting Bracket
            ProductComponent(product_id=5, component_id=10, quantity_required=5), # Sensor Array
        ])
        
        db.add_all(product_components)
        db.commit()
        
        # Create inventory
        print("Creating inventory...")
        inventory_items = []
        
        # More realistic inventory levels with some low stock items
        inventory_data = [
            (1, 85, 15, 30, "Warehouse A, Aisle 1, Shelf 5"),   # Steel Frame - moderate
            (2, 250, 50, 100, "Warehouse A, Aisle 2, Shelf 10"), # Rubber Gasket - good stock
            (3, 120, 40, 50, "Warehouse B, Aisle 3, Shelf 8"),   # Circuit Board - moderate
            (4, 65, 20, 30, "Warehouse B, Aisle 4, Shelf 3"),     # Power Supply - low
            (5, 45, 10, 25, "Warehouse B, Aisle 5, Shelf 2"),     # LCD Display - low
            (6, 95, 25, 40, "Warehouse A, Aisle 6, Shelf 6"),    # Aluminum Housing - moderate
            (7, 180, 35, 60, "Warehouse A, Aisle 7, Shelf 12"), # Cooling Fan - good stock
            (8, 110, 30, 45, "Warehouse B, Aisle 8, Shelf 7"),  # Wiring Harness - moderate
            (9, 200, 40, 80, "Warehouse A, Aisle 9, Shelf 15"),  # Mounting Bracket - good stock
            (10, 70, 15, 30, "Warehouse B, Aisle 10, Shelf 4")  # Sensor Array - moderate
        ]
        
        for component_id, quantity, allocated, threshold, location in inventory_data:
            inventory_items.append(
                InventoryItem(
                    component_id=component_id,
                    quantity_available=quantity,
                    quantity_allocated=allocated,
                    reorder_threshold=threshold,
                    location=location
                )
            )
        
        db.add_all(inventory_items)
        db.commit()
        
        # Create suppliers
        print("Creating suppliers...")
        suppliers = [
            Supplier(
                name="TechParts Inc.",
                contact_person="Robert Chen",
                email="robert.chen@techparts.com",
                phone="555-111-2222",
                address="100 Technology Pkwy, San Jose, USA",
                reliability=SupplierReliability.HIGH
            ),
            Supplier(
                name="Global Materials Co.",
                contact_person="Sarah Johnson",
                email="sarah.johnson@globalmaterials.com",
                phone="555-333-4444",
                address="200 Industrial Blvd, Detroit, USA",
                reliability=SupplierReliability.MEDIUM
            ),
            Supplier(
                name="Eastern Electronics",
                contact_person="Wei Zhang",
                email="wei.zhang@easternelec.com",
                phone="555-555-6666",
                address="123 Manufacturing Rd, Shenzhen, China",
                reliability=SupplierReliability.HIGH
            ),
            Supplier(
                name="MetalWorks Ltd.",
                contact_person="James Wilson",
                email="james.wilson@metalworks.com",
                phone="555-777-8888",
                address="50 Steel St, Pittsburgh, USA",
                reliability=SupplierReliability.MEDIUM
            ),
            Supplier(
                name="CircuitTech",
                contact_person="Maria Garcia",
                email="maria.garcia@circuittech.com",
                phone="555-999-0000",
                address="75 Electronics Way, Taipei, Taiwan",
                reliability=SupplierReliability.LOW
            )
        ]
        db.add_all(suppliers)
        db.commit()
        
        # Create supplier components
        print("Creating supplier components...")
        supplier_components = []
        
        # TechParts Inc. supplies electronic components
        supplier_components.extend([
            SupplierComponent(supplier_id=1, component_id=3, lead_time_days=14, unit_price=45.00, minimum_order=10),  # Circuit Board
            SupplierComponent(supplier_id=1, component_id=4, lead_time_days=10, unit_price=65.00, minimum_order=5),   # Power Supply
            SupplierComponent(supplier_id=1, component_id=5, lead_time_days=21, unit_price=85.00, minimum_order=5),   # LCD Display
            SupplierComponent(supplier_id=1, component_id=7, lead_time_days=7, unit_price=25.00, minimum_order=20),   # Cooling Fan
        ])
        
        # Global Materials Co. supplies various materials
        supplier_components.extend([
            SupplierComponent(supplier_id=2, component_id=2, lead_time_days=5, unit_price=3.50, minimum_order=100),   # Rubber Gasket
            SupplierComponent(supplier_id=2, component_id=6, lead_time_days=14, unit_price=35.00, minimum_order=10),  # Aluminum Housing
            SupplierComponent(supplier_id=2, component_id=9, lead_time_days=7, unit_price=12.00, minimum_order=25),   # Mounting Bracket
        ])
        
        # Eastern Electronics supplies electronic components
        supplier_components.extend([
            SupplierComponent(supplier_id=3, component_id=3, lead_time_days=30, unit_price=40.00, minimum_order=20),  # Circuit Board
            SupplierComponent(supplier_id=3, component_id=5, lead_time_days=25, unit_price=75.00, minimum_order=10),  # LCD Display
            SupplierComponent(supplier_id=3, component_id=8, lead_time_days=15, unit_price=18.00, minimum_order=15),  # Wiring Harness
            SupplierComponent(supplier_id=3, component_id=10, lead_time_days=21, unit_price=55.00, minimum_order=5),  # Sensor Array
        ])
        
        # MetalWorks Ltd. supplies metal components
        supplier_components.extend([
            SupplierComponent(supplier_id=4, component_id=1, lead_time_days=21, unit_price=120.00, minimum_order=5),  # Steel Frame
            SupplierComponent(supplier_id=4, component_id=6, lead_time_days=18, unit_price=40.00, minimum_order=10),  # Aluminum Housing
            SupplierComponent(supplier_id=4, component_id=9, lead_time_days=10, unit_price=15.00, minimum_order=20),  # Mounting Bracket
        ])
        
        # CircuitTech supplies electronic components
        supplier_components.extend([
            SupplierComponent(supplier_id=5, component_id=3, lead_time_days=10, unit_price=38.00, minimum_order=15),  # Circuit Board
            SupplierComponent(supplier_id=5, component_id=7, lead_time_days=5, unit_price=20.00, minimum_order=25),   # Cooling Fan
            SupplierComponent(supplier_id=5, component_id=8, lead_time_days=7, unit_price=15.00, minimum_order=20),   # Wiring Harness
            SupplierComponent(supplier_id=5, component_id=10, lead_time_days=14, unit_price=50.00, minimum_order=10), # Sensor Array
        ])
        
        db.add_all(supplier_components)
        db.commit()
        
        # Create production lines
        print("Creating production lines...")
        production_lines = [
            ProductionLine(
                name="Assembly Line A",
                description="Main assembly line for large products",
                capacity_per_hour=5,
                is_active=True
            ),
            ProductionLine(
                name="Assembly Line B",
                description="Secondary assembly line for medium products",
                capacity_per_hour=8,
                is_active=True
            ),
            ProductionLine(
                name="Electronics Line",
                description="Specialized line for electronic components",
                capacity_per_hour=12,
                is_active=True
            ),
            ProductionLine(
                name="Testing Line",
                description="Quality control and testing",
                capacity_per_hour=15,
                is_active=True
            ),
            ProductionLine(
                name="Packaging Line",
                description="Final packaging and preparation",
                capacity_per_hour=20,
                is_active=True
            )
        ]
        db.add_all(production_lines)
        db.commit()
        
        # Create orders
        print("Creating orders...")
        now = datetime.utcnow()
        
        orders = [
            # Historical orders
            Order(
                customer_id=1,
                order_date=now - timedelta(days=60),
                status=OrderStatus.DELIVERED,
                estimated_delivery=now - timedelta(days=40),
                actual_delivery=now - timedelta(days=39),
                notes="Regular order, delivered on time"
            ),
            Order(
                customer_id=2,
                order_date=now - timedelta(days=50),
                status=OrderStatus.DELIVERED,
                estimated_delivery=now - timedelta(days=30),
                actual_delivery=now - timedelta(days=29),
                notes="Bulk order completed successfully"
            ),
            Order(
                customer_id=3,
                order_date=now - timedelta(days=45),
                status=OrderStatus.DELIVERED,
                estimated_delivery=now - timedelta(days=25),
                actual_delivery=now - timedelta(days=24),
                notes="Custom configuration delivered"
            ),
            # Recent completed orders
            Order(
                customer_id=1,
                order_date=now - timedelta(days=30),
                status=OrderStatus.DELIVERED,
                estimated_delivery=now - timedelta(days=10),
                actual_delivery=now - timedelta(days=9),
                notes="Regular order, delivered on time"
            ),
            Order(
                customer_id=2,
                order_date=now - timedelta(days=20),
                status=OrderStatus.SHIPPED,
                estimated_delivery=now + timedelta(days=5),
                notes="Expedited shipping requested"
            ),
            # Active orders
            Order(
                customer_id=3,
                order_date=now - timedelta(days=15),
                status=OrderStatus.IN_PRODUCTION,
                estimated_delivery=now + timedelta(days=15),
                notes="Custom configuration requested"
            ),
            Order(
                customer_id=4,
                order_date=now - timedelta(days=10),
                status=OrderStatus.IN_PRODUCTION,
                estimated_delivery=now + timedelta(days=20),
                notes="Large order in progress"
            ),
            # Confirmed orders (ready for optimization)
            Order(
                customer_id=4,
                order_date=now - timedelta(days=5),
                status=OrderStatus.CONFIRMED,
                estimated_delivery=now + timedelta(days=25),
                notes="Standard order - ready for production"
            ),
            Order(
                customer_id=1,
                order_date=now - timedelta(days=3),
                status=OrderStatus.CONFIRMED,
                estimated_delivery=now + timedelta(days=27),
                notes="Priority order - needs scheduling"
            ),
            Order(
                customer_id=2,
                order_date=now - timedelta(days=2),
                status=OrderStatus.CONFIRMED,
                estimated_delivery=now + timedelta(days=28),
                notes="Bulk order - optimize for cost"
            ),
            Order(
                customer_id=5,
                order_date=now - timedelta(days=1),
                status=OrderStatus.CONFIRMED,
                estimated_delivery=now + timedelta(days=30),
                notes="New order - awaiting optimization"
            ),
            # Pending orders
            Order(
                customer_id=5,
                order_date=now - timedelta(days=1),
                status=OrderStatus.PENDING,
                estimated_delivery=now + timedelta(days=30),
                notes="Awaiting component availability confirmation"
            ),
            Order(
                customer_id=3,
                order_date=now,
                status=OrderStatus.PENDING,
                estimated_delivery=now + timedelta(days=35),
                notes="New order - pending feasibility check"
            ),
            Order(
                customer_id=1,
                order_date=now,
                status=OrderStatus.PENDING,
                estimated_delivery=now + timedelta(days=40),
                notes="Large custom order - under review"
            )
        ]
        db.add_all(orders)
        db.commit()
        
        # Create order items
        print("Creating order items...")
        order_items = [
            # Historical orders
            OrderItem(order_id=1, product_id=1, quantity=2, unit_price=1299.99),
            OrderItem(order_id=1, product_id=3, quantity=1, unit_price=3499.99),
            OrderItem(order_id=2, product_id=2, quantity=10, unit_price=249.99),
            OrderItem(order_id=2, product_id=5, quantity=5, unit_price=899.99),
            OrderItem(order_id=3, product_id=4, quantity=3, unit_price=1899.99),
            
            # Recent completed
            OrderItem(order_id=4, product_id=1, quantity=2, unit_price=1299.99),
            OrderItem(order_id=4, product_id=3, quantity=1, unit_price=3499.99),
            OrderItem(order_id=5, product_id=2, quantity=10, unit_price=249.99),
            OrderItem(order_id=5, product_id=5, quantity=5, unit_price=899.99),
            
            # Active production
            OrderItem(order_id=6, product_id=4, quantity=3, unit_price=1899.99),
            OrderItem(order_id=7, product_id=1, quantity=5, unit_price=1299.99),
            OrderItem(order_id=7, product_id=2, quantity=8, unit_price=249.99),
            
            # Confirmed (ready for optimization)
            OrderItem(order_id=8, product_id=1, quantity=1, unit_price=1299.99),
            OrderItem(order_id=8, product_id=2, quantity=5, unit_price=249.99),
            OrderItem(order_id=8, product_id=5, quantity=2, unit_price=899.99),
            OrderItem(order_id=9, product_id=3, quantity=2, unit_price=3499.99),
            OrderItem(order_id=9, product_id=4, quantity=1, unit_price=1899.99),
            OrderItem(order_id=10, product_id=2, quantity=15, unit_price=249.99),
            OrderItem(order_id=10, product_id=5, quantity=10, unit_price=899.99),
            OrderItem(order_id=11, product_id=1, quantity=3, unit_price=1299.99),
            OrderItem(order_id=11, product_id=3, quantity=1, unit_price=3499.99),
            
            # Pending
            OrderItem(order_id=12, product_id=3, quantity=2, unit_price=3499.99),
            OrderItem(order_id=12, product_id=4, quantity=4, unit_price=1899.99),
            OrderItem(order_id=13, product_id=1, quantity=4, unit_price=1299.99),
            OrderItem(order_id=13, product_id=2, quantity=12, unit_price=249.99),
            OrderItem(order_id=14, product_id=3, quantity=3, unit_price=3499.99),
            OrderItem(order_id=14, product_id=4, quantity=2, unit_price=1899.99),
            OrderItem(order_id=14, product_id=5, quantity=8, unit_price=899.99)
        ]
        db.add_all(order_items)
        db.commit()
        
        # Create production schedules
        print("Creating production schedules...")
        production_schedules = [
            # Historical completed schedules
            ProductionSchedule(
                order_id=1,
                production_line_id=1,
                scheduled_start=now - timedelta(days=55),
                scheduled_end=now - timedelta(days=50),
                actual_start=now - timedelta(days=55),
                actual_end=now - timedelta(days=49),
                status="completed",
                notes="Completed ahead of schedule"
            ),
            ProductionSchedule(
                order_id=2,
                production_line_id=3,
                scheduled_start=now - timedelta(days=45),
                scheduled_end=now - timedelta(days=40),
                actual_start=now - timedelta(days=45),
                actual_end=now - timedelta(days=40),
                status="completed",
                notes="Completed on schedule"
            ),
            ProductionSchedule(
                order_id=3,
                production_line_id=2,
                scheduled_start=now - timedelta(days=40),
                scheduled_end=now - timedelta(days=35),
                actual_start=now - timedelta(days=40),
                actual_end=now - timedelta(days=34),
                status="completed",
                notes="Quality check passed"
            ),
            # Recent completed
            ProductionSchedule(
                order_id=4,
                production_line_id=1,
                scheduled_start=now - timedelta(days=25),
                scheduled_end=now - timedelta(days=20),
                actual_start=now - timedelta(days=25),
                actual_end=now - timedelta(days=19),
                status="completed",
                notes="Completed ahead of schedule"
            ),
            ProductionSchedule(
                order_id=5,
                production_line_id=3,
                scheduled_start=now - timedelta(days=15),
                scheduled_end=now - timedelta(days=10),
                actual_start=now - timedelta(days=15),
                actual_end=now - timedelta(days=10),
                status="completed",
                notes="Completed on schedule"
            ),
            # Active production
            ProductionSchedule(
                order_id=6,
                production_line_id=1,
                scheduled_start=now - timedelta(days=5),
                scheduled_end=now + timedelta(days=5),
                actual_start=now - timedelta(days=5),
                status="in_progress",
                notes="Production proceeding normally"
            ),
            ProductionSchedule(
                order_id=7,
                production_line_id=2,
                scheduled_start=now - timedelta(days=3),
                scheduled_end=now + timedelta(days=7),
                actual_start=now - timedelta(days=3),
                status="in_progress",
                notes="Large order in progress"
            ),
            # Scheduled (ready to start)
            ProductionSchedule(
                order_id=8,
                production_line_id=2,
                scheduled_start=now + timedelta(days=5),
                scheduled_end=now + timedelta(days=15),
                status="scheduled",
                notes="Awaiting start - confirmed order"
            )
            # Orders 9-14 are confirmed/pending and need optimization
        ]
        db.add_all(production_schedules)
        db.commit()
        
        # Create shipments
        print("Creating shipments...")
        shipments = [
            # Historical delivered shipments
            Shipment(
                supplier_id=1,
                expected_arrival=now - timedelta(days=30),
                actual_arrival=now - timedelta(days=30),
                status="delivered",
                tracking_number="TRK111111111",
                shipping_method="Ground",
                notes="Regular delivery"
            ),
            Shipment(
                supplier_id=2,
                expected_arrival=now - timedelta(days=25),
                actual_arrival=now - timedelta(days=24),
                status="delivered",
                tracking_number="TRK222222222",
                shipping_method="Ground",
                notes="On-time delivery"
            ),
            # Recent delivered
            Shipment(
                supplier_id=1,
                expected_arrival=now - timedelta(days=5),
                actual_arrival=now - timedelta(days=5),
                status="delivered",
                tracking_number="TRK123456789",
                shipping_method="Ground",
                notes="Regular delivery"
            ),
            Shipment(
                supplier_id=3,
                expected_arrival=now - timedelta(days=3),
                actual_arrival=now - timedelta(days=2),
                status="delivered",
                tracking_number="TRK333333333",
                shipping_method="Air",
                notes="Expedited delivery"
            ),
            # In transit shipments
            Shipment(
                supplier_id=3,
                expected_arrival=now + timedelta(days=10),
                status="in_transit",
                tracking_number="TRK987654321",
                shipping_method="Air",
                notes="Expedited shipping"
            ),
            Shipment(
                supplier_id=1,
                expected_arrival=now + timedelta(days=7),
                status="in_transit",
                tracking_number="TRK444444444",
                shipping_method="Ground",
                notes="Standard shipping"
            ),
            Shipment(
                supplier_id=4,
                expected_arrival=now + timedelta(days=12),
                status="in_transit",
                tracking_number="TRK555555555",
                shipping_method="Ground",
                notes="Bulk materials"
            ),
            # Scheduled shipments
            Shipment(
                supplier_id=4,
                expected_arrival=now + timedelta(days=20),
                status="scheduled",
                tracking_number="TRK456789123",
                shipping_method="Ocean",
                notes="Bulk shipment"
            ),
            Shipment(
                supplier_id=2,
                expected_arrival=now + timedelta(days=25),
                status="scheduled",
                tracking_number="TRK666666666",
                shipping_method="Ground",
                notes="Scheduled delivery"
            ),
            # Delayed shipments
            Shipment(
                supplier_id=2,
                expected_arrival=now - timedelta(days=2),
                status="delayed",
                tracking_number="TRK789123456",
                shipping_method="Ground",
                notes="Delayed due to weather"
            ),
            Shipment(
                supplier_id=5,
                expected_arrival=now - timedelta(days=1),
                status="delayed",
                tracking_number="TRK777777777",
                shipping_method="Air",
                notes="Customs delay"
            ),
            # Processing shipments
            Shipment(
                supplier_id=5,
                expected_arrival=now + timedelta(days=15),
                status="processing",
                tracking_number=None,
                shipping_method="Air",
                notes="Order being processed by supplier"
            ),
            Shipment(
                supplier_id=3,
                expected_arrival=now + timedelta(days=18),
                status="processing",
                tracking_number=None,
                shipping_method="Ocean",
                notes="Awaiting supplier confirmation"
            )
        ]
        db.add_all(shipments)
        db.commit()
        
        # Create shipment items
        print("Creating shipment items...")
        shipment_items = [
            # Historical shipments
            ShipmentItem(shipment_id=1, component_id=3, quantity=50),  # Circuit Board
            ShipmentItem(shipment_id=1, component_id=4, quantity=20),  # Power Supply
            ShipmentItem(shipment_id=2, component_id=2, quantity=150), # Rubber Gasket
            ShipmentItem(shipment_id=2, component_id=6, quantity=25),  # Aluminum Housing
            
            # Recent delivered
            ShipmentItem(shipment_id=3, component_id=3, quantity=50),  # Circuit Board
            ShipmentItem(shipment_id=3, component_id=4, quantity=20),  # Power Supply
            ShipmentItem(shipment_id=3, component_id=7, quantity=40),  # Cooling Fan
            ShipmentItem(shipment_id=4, component_id=5, quantity=30),  # LCD Display
            ShipmentItem(shipment_id=4, component_id=10, quantity=20), # Sensor Array
            
            # In transit
            ShipmentItem(shipment_id=5, component_id=3, quantity=30),  # Circuit Board
            ShipmentItem(shipment_id=5, component_id=5, quantity=25),  # LCD Display
            ShipmentItem(shipment_id=5, component_id=10, quantity=15), # Sensor Array
            ShipmentItem(shipment_id=6, component_id=4, quantity=15),  # Power Supply
            ShipmentItem(shipment_id=6, component_id=7, quantity=35),  # Cooling Fan
            ShipmentItem(shipment_id=7, component_id=1, quantity=10),  # Steel Frame
            ShipmentItem(shipment_id=7, component_id=6, quantity=15),  # Aluminum Housing
            
            # Scheduled
            ShipmentItem(shipment_id=8, component_id=1, quantity=15),  # Steel Frame
            ShipmentItem(shipment_id=8, component_id=6, quantity=20),  # Aluminum Housing
            ShipmentItem(shipment_id=9, component_id=2, quantity=180), # Rubber Gasket
            ShipmentItem(shipment_id=9, component_id=9, quantity=45),  # Mounting Bracket
            
            # Delayed
            ShipmentItem(shipment_id=10, component_id=2, quantity=200), # Rubber Gasket
            ShipmentItem(shipment_id=10, component_id=9, quantity=50),  # Mounting Bracket
            ShipmentItem(shipment_id=11, component_id=3, quantity=25),  # Circuit Board
            ShipmentItem(shipment_id=11, component_id=8, quantity=20),  # Wiring Harness
            
            # Processing
            ShipmentItem(shipment_id=12, component_id=3, quantity=40),  # Circuit Board
            ShipmentItem(shipment_id=12, component_id=8, quantity=30),  # Wiring Harness
            ShipmentItem(shipment_id=12, component_id=10, quantity=20), # Sensor Array
            ShipmentItem(shipment_id=13, component_id=1, quantity=20),  # Steel Frame
            ShipmentItem(shipment_id=13, component_id=4, quantity=25),  # Power Supply
        ]
        db.add_all(shipment_items)
        db.commit()
        
        # Create external risks
        print("Creating external risks...")
        external_risks = [
            # Weather risk
            ExternalRisk(
                risk_type="weather",
                region="Southeast Asia",
                description="Tropical storm approaching manufacturing hubs",
                risk_level=RiskLevel.HIGH,
                start_date=now,
                end_date=now + timedelta(days=5),
                data={
                    "storm_name": "Typhoon Megi",
                    "wind_speed": 120,
                    "rainfall_mm": 300,
                    "affected_areas": ["Vietnam", "Thailand", "Malaysia"]
                }
            ),
            
            # Logistics risk
            ExternalRisk(
                risk_type="logistics",
                region="Asia Pacific",
                description="Port congestion at Shanghai port",
                risk_level=RiskLevel.MEDIUM,
                start_date=now,
                end_date=now + timedelta(days=10),
                data={
                    "port_name": "Shanghai",
                    "congestion_level": "High",
                    "average_delay_days": 7,
                    "vessels_waiting": 38
                }
            ),
            
            # Market risk
            ExternalRisk(
                risk_type="market",
                region="Global",
                description="Semiconductor shortage affecting electronics supply",
                risk_level=RiskLevel.CRITICAL,
                start_date=now,
                end_date=now + timedelta(days=90),
                data={
                    "commodity": "Semiconductors",
                    "price_increase_percent": 35,
                    "estimated_shortage_months": 6
                }
            ),
            
            # Geopolitical risk
            ExternalRisk(
                risk_type="geopolitical",
                region="Eastern Europe",
                description="Trade restrictions affecting material exports",
                risk_level=RiskLevel.HIGH,
                start_date=now,
                end_date=None,  # Indefinite
                data={
                    "countries_affected": ["Multiple Eastern European countries"],
                    "materials_affected": ["Metals", "Energy"],
                    "policy_type": "Export controls"
                }
            )
        ]
        db.add_all(external_risks)
        db.commit()
        
        # Create staff members
        print("Creating staff members...")
        staff_members = [
            Staff(
                name="John Anderson",
                employee_id="EMP001",
                department="production",
                skill_level="expert",
                specialization="Assembly",
                hourly_rate=45.00,
                is_available=True,
                max_hours_per_day=8,
                current_workload_hours=6.0
            ),
            Staff(
                name="Sarah Martinez",
                employee_id="EMP002",
                department="production",
                skill_level="senior",
                specialization="Welding",
                hourly_rate=38.00,
                is_available=True,
                max_hours_per_day=8,
                current_workload_hours=4.0
            ),
            Staff(
                name="Michael Chen",
                employee_id="EMP003",
                department="production",
                skill_level="senior",
                specialization="Electronics Assembly",
                hourly_rate=40.00,
                is_available=True,
                max_hours_per_day=8,
                current_workload_hours=5.5
            ),
            Staff(
                name="Emily Johnson",
                employee_id="EMP004",
                department="quality",
                skill_level="expert",
                specialization="Quality Control",
                hourly_rate=42.00,
                is_available=True,
                max_hours_per_day=8,
                current_workload_hours=3.0
            ),
            Staff(
                name="David Wilson",
                employee_id="EMP005",
                department="production",
                skill_level="intermediate",
                specialization="Assembly",
                hourly_rate=28.00,
                is_available=True,
                max_hours_per_day=8,
                current_workload_hours=2.0
            ),
            Staff(
                name="Lisa Brown",
                employee_id="EMP006",
                department="production",
                skill_level="intermediate",
                specialization="Packaging",
                hourly_rate=25.00,
                is_available=True,
                max_hours_per_day=8,
                current_workload_hours=1.5
            ),
            Staff(
                name="Robert Taylor",
                employee_id="EMP007",
                department="maintenance",
                skill_level="senior",
                specialization="Equipment Maintenance",
                hourly_rate=35.00,
                is_available=True,
                max_hours_per_day=8,
                current_workload_hours=0.0
            ),
            Staff(
                name="Jennifer Davis",
                employee_id="EMP008",
                department="production",
                skill_level="junior",
                specialization="Assembly",
                hourly_rate=22.00,
                is_available=True,
                max_hours_per_day=8,
                current_workload_hours=0.0
            ),
            Staff(
                name="James Miller",
                employee_id="EMP009",
                department="production",
                skill_level="senior",
                specialization="Testing",
                hourly_rate=36.00,
                is_available=True,
                max_hours_per_day=8,
                current_workload_hours=4.5
            ),
            Staff(
                name="Patricia Garcia",
                employee_id="EMP010",
                department="logistics",
                skill_level="intermediate",
                specialization="Material Handling",
                hourly_rate=26.00,
                is_available=True,
                max_hours_per_day=8,
                current_workload_hours=2.0
            ),
            Staff(
                name="William Rodriguez",
                employee_id="EMP011",
                department="production",
                skill_level="expert",
                specialization="Complex Assembly",
                hourly_rate=48.00,
                is_available=True,
                max_hours_per_day=8,
                current_workload_hours=7.0
            ),
            Staff(
                name="Mary Martinez",
                employee_id="EMP012",
                department="quality",
                skill_level="senior",
                specialization="Quality Control",
                hourly_rate=37.00,
                is_available=True,
                max_hours_per_day=8,
                current_workload_hours=3.5
            ),
            Staff(
                name="Richard Lee",
                employee_id="EMP013",
                department="production",
                skill_level="intermediate",
                specialization="Electronics Assembly",
                hourly_rate=30.00,
                is_available=True,
                max_hours_per_day=8,
                current_workload_hours=1.0
            ),
            Staff(
                name="Susan White",
                employee_id="EMP014",
                department="production",
                skill_level="junior",
                specialization="Packaging",
                hourly_rate=23.00,
                is_available=True,
                max_hours_per_day=8,
                current_workload_hours=0.5
            ),
            Staff(
                name="Joseph Harris",
                employee_id="EMP015",
                department="maintenance",
                skill_level="expert",
                specialization="Equipment Maintenance",
                hourly_rate=44.00,
                is_available=False,  # On leave
                max_hours_per_day=8,
                current_workload_hours=0.0
            )
        ]
        db.add_all(staff_members)
        db.commit()
        
        # Create task assignments
        print("Creating task assignments...")
        task_assignments = [
            # Assignments for active production schedules
            TaskAssignment(
                production_schedule_id=6,  # Order 6 - in progress
                staff_id=1,  # John Anderson
                task_type="production",
                assigned_hours=40.0,
                start_time=now - timedelta(days=5),
                end_time=now + timedelta(days=5),
                status="in_progress",
                notes="Main assembly work"
            ),
            TaskAssignment(
                production_schedule_id=6,
                staff_id=4,  # Emily Johnson
                task_type="quality_check",
                assigned_hours=8.0,
                start_time=now + timedelta(days=3),
                end_time=now + timedelta(days=5),
                status="assigned",
                notes="Final quality inspection"
            ),
            TaskAssignment(
                production_schedule_id=7,  # Order 7 - in progress
                staff_id=2,  # Sarah Martinez
                task_type="production",
                assigned_hours=50.0,
                start_time=now - timedelta(days=3),
                end_time=now + timedelta(days=7),
                status="in_progress",
                notes="Welding and assembly"
            ),
            TaskAssignment(
                production_schedule_id=7,
                staff_id=3,  # Michael Chen
                task_type="production",
                assigned_hours=45.0,
                start_time=now - timedelta(days=2),
                end_time=now + timedelta(days=6),
                status="in_progress",
                notes="Electronics integration"
            ),
            TaskAssignment(
                production_schedule_id=7,
                staff_id=9,  # James Miller
                task_type="quality_check",
                assigned_hours=12.0,
                start_time=now + timedelta(days=5),
                end_time=now + timedelta(days=7),
                status="assigned",
                notes="Testing and validation"
            ),
            # Assignment for scheduled production
            TaskAssignment(
                production_schedule_id=8,  # Order 8 - scheduled
                staff_id=5,  # David Wilson
                task_type="production",
                assigned_hours=60.0,
                start_time=now + timedelta(days=5),
                end_time=now + timedelta(days=15),
                status="assigned",
                notes="Scheduled assembly work"
            ),
            TaskAssignment(
                production_schedule_id=8,
                staff_id=6,  # Lisa Brown
                task_type="production",
                assigned_hours=40.0,
                start_time=now + timedelta(days=10),
                end_time=now + timedelta(days=15),
                status="assigned",
                notes="Packaging and preparation"
            )
        ]
        db.add_all(task_assignments)
        db.commit()
        
        # Create users
        print("Creating users...")
        users = [
            User(
                username="admin",
                email="admin@example.com",
                hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # password: secret
                full_name="Admin User",
                department="IT",
                role="admin",
                is_active=True
            ),
            User(
                username="sales_manager",
                email="sales@example.com",
                hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # password: secret
                full_name="Sales Manager",
                department="Sales",
                role="manager",
                is_active=True
            ),
            User(
                username="production_manager",
                email="production@example.com",
                hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # password: secret
                full_name="Production Manager",
                department="Production",
                role="manager",
                is_active=True
            ),
            User(
                username="inventory_manager",
                email="inventory@example.com",
                hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # password: secret
                full_name="Inventory Manager",
                department="Inventory",
                role="manager",
                is_active=True
            ),
            User(
                username="sales_rep",
                email="salesrep@example.com",
                hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # password: secret
                full_name="Sales Representative",
                department="Sales",
                role="sales",
                is_active=True
            )
        ]
        db.add_all(users)
        db.commit()
        
        print("Database seeded successfully!")
    
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()