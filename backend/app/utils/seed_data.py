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
    OrderStatus, SupplierReliability, RiskLevel
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
        
        for component_id in range(1, 11):
            # Random inventory levels
            quantity = random.randint(50, 200)
            allocated = random.randint(0, min(30, quantity))
            threshold = random.randint(20, 40)
            
            inventory_items.append(
                InventoryItem(
                    component_id=component_id,
                    quantity_available=quantity,
                    quantity_allocated=allocated,
                    reorder_threshold=threshold,
                    location=f"Warehouse A, Aisle {random.randint(1, 10)}, Shelf {random.randint(1, 20)}"
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
            Order(
                customer_id=3,
                order_date=now - timedelta(days=15),
                status=OrderStatus.IN_PRODUCTION,
                estimated_delivery=now + timedelta(days=15),
                notes="Custom configuration requested"
            ),
            Order(
                customer_id=4,
                order_date=now - timedelta(days=5),
                status=OrderStatus.CONFIRMED,
                estimated_delivery=now + timedelta(days=25),
                notes="Standard order"
            ),
            Order(
                customer_id=5,
                order_date=now - timedelta(days=1),
                status=OrderStatus.PENDING,
                estimated_delivery=now + timedelta(days=30),
                notes="Awaiting component availability confirmation"
            )
        ]
        db.add_all(orders)
        db.commit()
        
        # Create order items
        print("Creating order items...")
        order_items = [
            # Order 1 (Delivered)
            OrderItem(order_id=1, product_id=1, quantity=2, unit_price=1299.99),
            OrderItem(order_id=1, product_id=3, quantity=1, unit_price=3499.99),
            
            # Order 2 (Shipped)
            OrderItem(order_id=2, product_id=2, quantity=10, unit_price=249.99),
            OrderItem(order_id=2, product_id=5, quantity=5, unit_price=899.99),
            
            # Order 3 (In Production)
            OrderItem(order_id=3, product_id=4, quantity=3, unit_price=1899.99),
            
            # Order 4 (Confirmed)
            OrderItem(order_id=4, product_id=1, quantity=1, unit_price=1299.99),
            OrderItem(order_id=4, product_id=2, quantity=5, unit_price=249.99),
            OrderItem(order_id=4, product_id=5, quantity=2, unit_price=899.99),
            
            # Order 5 (Pending)
            OrderItem(order_id=5, product_id=3, quantity=2, unit_price=3499.99),
            OrderItem(order_id=5, product_id=4, quantity=4, unit_price=1899.99)
        ]
        db.add_all(order_items)
        db.commit()
        
        # Create production schedules
        print("Creating production schedules...")
        production_schedules = [
            # Order 1 (Delivered) - Historical production
            ProductionSchedule(
                order_id=1,
                production_line_id=1,
                scheduled_start=now - timedelta(days=25),
                scheduled_end=now - timedelta(days=20),
                actual_start=now - timedelta(days=25),
                actual_end=now - timedelta(days=19),
                status="completed",
                notes="Completed ahead of schedule"
            ),
            
            # Order 2 (Shipped) - Completed production
            ProductionSchedule(
                order_id=2,
                production_line_id=3,
                scheduled_start=now - timedelta(days=15),
                scheduled_end=now - timedelta(days=10),
                actual_start=now - timedelta(days=15),
                actual_end=now - timedelta(days=10),
                status="completed",
                notes="Completed on schedule"
            ),
            
            # Order 3 (In Production) - Active production
            ProductionSchedule(
                order_id=3,
                production_line_id=1,
                scheduled_start=now - timedelta(days=5),
                scheduled_end=now + timedelta(days=5),
                actual_start=now - timedelta(days=5),
                status="in_progress",
                notes="Production proceeding normally"
            ),
            
            # Order 4 (Confirmed) - Scheduled production
            ProductionSchedule(
                order_id=4,
                production_line_id=2,
                scheduled_start=now + timedelta(days=5),
                scheduled_end=now + timedelta(days=15),
                status="scheduled",
                notes="Awaiting start"
            ),
            
            # Order 5 (Pending) - Not yet scheduled
        ]
        db.add_all(production_schedules)
        db.commit()
        
        # Create shipments
        print("Creating shipments...")
        shipments = [
            # Incoming shipment 1 - Arrived
            Shipment(
                supplier_id=1,
                expected_arrival=now - timedelta(days=5),
                actual_arrival=now - timedelta(days=5),
                status="delivered",
                tracking_number="TRK123456789",
                shipping_method="Ground",
                notes="Regular delivery"
            ),
            
            # Incoming shipment 2 - In transit
            Shipment(
                supplier_id=3,
                expected_arrival=now + timedelta(days=10),
                status="in_transit",
                tracking_number="TRK987654321",
                shipping_method="Air",
                notes="Expedited shipping"
            ),
            
            # Incoming shipment 3 - Scheduled
            Shipment(
                supplier_id=4,
                expected_arrival=now + timedelta(days=20),
                status="scheduled",
                tracking_number="TRK456789123",
                shipping_method="Ocean",
                notes="Bulk shipment"
            ),
            
            # Incoming shipment 4 - Delayed
            Shipment(
                supplier_id=2,
                expected_arrival=now - timedelta(days=2),
                status="delayed",
                tracking_number="TRK789123456",
                shipping_method="Ground",
                notes="Delayed due to weather"
            ),
            
            # Incoming shipment 5 - Processing
            Shipment(
                supplier_id=5,
                expected_arrival=now + timedelta(days=15),
                status="processing",
                tracking_number=None,
                shipping_method="Air",
                notes="Order being processed by supplier"
            )
        ]
        db.add_all(shipments)
        db.commit()
        
        # Create shipment items
        print("Creating shipment items...")
        shipment_items = [
            # Shipment 1 items (Delivered)
            ShipmentItem(shipment_id=1, component_id=3, quantity=50),  # Circuit Board
            ShipmentItem(shipment_id=1, component_id=4, quantity=20),  # Power Supply
            ShipmentItem(shipment_id=1, component_id=7, quantity=40),  # Cooling Fan
            
            # Shipment 2 items (In Transit)
            ShipmentItem(shipment_id=2, component_id=3, quantity=30),  # Circuit Board
            ShipmentItem(shipment_id=2, component_id=5, quantity=25),  # LCD Display
            ShipmentItem(shipment_id=2, component_id=10, quantity=15), # Sensor Array
            
            # Shipment 3 items (Scheduled)
            ShipmentItem(shipment_id=3, component_id=1, quantity=15),  # Steel Frame
            ShipmentItem(shipment_id=3, component_id=6, quantity=20),  # Aluminum Housing
            
            # Shipment 4 items (Delayed)
            ShipmentItem(shipment_id=4, component_id=2, quantity=200), # Rubber Gasket
            ShipmentItem(shipment_id=4, component_id=9, quantity=50),  # Mounting Bracket
            
            # Shipment 5 items (Processing)
            ShipmentItem(shipment_id=5, component_id=3, quantity=40),  # Circuit Board
            ShipmentItem(shipment_id=5, component_id=8, quantity=30),  # Wiring Harness
            ShipmentItem(shipment_id=5, component_id=10, quantity=20)  # Sensor Array
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