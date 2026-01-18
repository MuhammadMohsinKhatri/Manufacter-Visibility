from app.services.order_service import OrderService
from app.services.inventory_service import (
    get_component, get_components, create_component,
    get_inventory_item, get_inventory_by_component, get_all_inventory,
    create_inventory_item, update_inventory_quantity, allocate_inventory,
    check_component_availability, check_product_components_availability,
    get_low_stock_items
)
from app.services.production_service import (
    get_production_line, get_production_lines, create_production_line,
    get_production_schedule, get_production_schedules, create_production_schedule,
    update_production_schedule, check_production_capacity, estimate_production_time
)
from app.services.risk_service import (
    get_external_risks, create_external_risk, update_external_risks,
    assess_supply_chain_risks
)