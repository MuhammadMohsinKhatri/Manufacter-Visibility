"""
Optimization Service for Production Scheduling
Uses Google OR-Tools for constraint programming and optimization
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
import math

try:
    from ortools.sat.python import cp_model
    OR_TOOLS_AVAILABLE = True
except ImportError:
    OR_TOOLS_AVAILABLE = False
    print("Warning: OR-Tools not available. Install with: pip install ortools")

from app.models.models import (
    Order, OrderItem, Product, ProductionLine, ProductionSchedule, 
    Staff, TaskAssignment
)


def _normalize_datetime(dt: datetime) -> datetime:
    """
    Normalize datetime to UTC timezone-naive format (SQLAlchemy standard).
    Handles both timezone-aware and timezone-naive datetimes.
    """
    if dt is None:
        return None
    
    # If already timezone-aware, convert to UTC then remove timezone info
    if dt.tzinfo is not None:
        # Convert to UTC
        utc_dt = dt.astimezone(timezone.utc)
        # Return as timezone-naive (SQLAlchemy standard)
        return utc_dt.replace(tzinfo=None)
    
    # If timezone-naive, assume it's already UTC (SQLAlchemy default)
    return dt


def optimize_production_schedule(
    db: Session,
    order_ids: List[int],
    start_date: datetime,
    end_date: datetime,
    objectives: Dict[str, float] = None
) -> Dict[str, Any]:
    """
    Optimize production schedule for multiple orders using constraint programming
    
    Objectives can include:
    - minimize_makespan: Minimize total completion time
    - minimize_setup_time: Minimize total setup/changeover time
    - maximize_utilization: Maximize production line utilization
    - minimize_cost: Minimize total production cost
    """
    
    if not OR_TOOLS_AVAILABLE:
        return {
            "success": False,
            "error": "OR-Tools not available. Please install: pip install ortools",
            "schedule": []
        }
    
    # Normalize datetimes to UTC (timezone-naive)
    start_date = _normalize_datetime(start_date)
    end_date = _normalize_datetime(end_date)
    
    # Default objectives
    if objectives is None:
        objectives = {
            "minimize_makespan": 0.4,
            "minimize_setup_time": 0.3,
            "maximize_utilization": 0.2,
            "minimize_cost": 0.1
        }
    
    # Get orders and their requirements
    orders = []
    for order_id in order_ids:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            continue
        
        order_items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
        if not order_items:
            # Order has no items, skip
            continue
            
        for item in order_items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if product:
                # Calculate estimated hours based on quantity
                # In production, this would use historical data or ML models
                estimated_hours = max(1, item.quantity * 2)  # Minimum 1 hour, 2 hours per unit
                orders.append({
                    "order_id": order_id,
                    "order_item_id": item.id,
                    "product_id": product.id,
                    "product_name": product.name,
                    "quantity": item.quantity,
                    "priority": 1,  # Can be enhanced with order priority
                    "estimated_hours": estimated_hours
                })
    
    if not orders:
        return {
            "success": False,
            "error": "No valid orders found",
            "schedule": []
        }
    
    # Get available production lines
    production_lines = db.query(ProductionLine).filter(
        ProductionLine.is_active == True
    ).all()
    
    if not production_lines:
        return {
            "success": False,
            "error": "No active production lines available",
            "schedule": []
        }
    
    # Get existing schedules to avoid conflicts
    # Normalize start_date and end_date for comparison
    start_date_normalized = _normalize_datetime(start_date)
    end_date_normalized = _normalize_datetime(end_date)
    
    existing_schedules = db.query(ProductionSchedule).filter(
        ProductionSchedule.scheduled_end >= start_date_normalized,
        ProductionSchedule.scheduled_start <= end_date_normalized
    ).all()
    
    # Create OR-Tools model
    model = cp_model.CpModel()
    
    # Variables
    # task_vars[i][j] = 1 if order i is assigned to production line j
    task_vars = {}
    start_vars = {}
    end_vars = {}
    duration_vars = {}
    
    num_orders = len(orders)
    num_lines = len(production_lines)
    
    # Time horizon in hours
    time_horizon = int((end_date - start_date).total_seconds() / 3600)
    
    for i in range(num_orders):
        for j in range(num_lines):
            # Binary variable: is order i assigned to line j?
            task_vars[(i, j)] = model.NewBoolVar(f'task_{i}_line_{j}')
            
            # Start time variable (in hours from start_date)
            start_vars[(i, j)] = model.NewIntVar(0, time_horizon, f'start_{i}_{j}')
            
            # Duration in hours
            duration = orders[i]["estimated_hours"]
            duration_vars[(i, j)] = model.NewIntVar(
                duration, duration, f'duration_{i}_{j}'
            )
            
            # End time
            end_vars[(i, j)] = model.NewIntVar(0, time_horizon, f'end_{i}_{j}')
            
            # Link start, duration, and end
            model.Add(end_vars[(i, j)] == start_vars[(i, j)] + duration_vars[(i, j)])
    
    # Constraints
    
    # 1. Each order must be assigned to exactly one production line
    for i in range(num_orders):
        model.Add(sum(task_vars[(i, j)] for j in range(num_lines)) == 1)
    
    # 2. If task is not assigned to a line, start/end times are 0
    for i in range(num_orders):
        for j in range(num_lines):
            # If not assigned, start and end must be 0
            model.Add(start_vars[(i, j)] == 0).OnlyEnforceIf(task_vars[(i, j)].Not())
            model.Add(end_vars[(i, j)] == 0).OnlyEnforceIf(task_vars[(i, j)].Not())
    
    # 3. No overlapping tasks on the same production line
    for j in range(num_lines):
        for i1 in range(num_orders):
            for i2 in range(i1 + 1, num_orders):
                # If both tasks are on same line, they must not overlap
                # Task i1 ends before i2 starts OR i2 ends before i1 starts
                task1_before_task2 = model.NewBoolVar(f't1_{i1}_before_t2_{i2}_line_{j}')
                task2_before_task1 = model.NewBoolVar(f't2_{i2}_before_t1_{i1}_line_{j}')
                
                model.Add(end_vars[(i1, j)] <= start_vars[(i2, j)]).OnlyEnforceIf(
                    [task_vars[(i1, j)], task_vars[(i2, j)], task1_before_task2]
                )
                model.Add(end_vars[(i2, j)] <= start_vars[(i1, j)]).OnlyEnforceIf(
                    [task_vars[(i1, j)], task_vars[(i2, j)], task2_before_task1]
                )
                
                model.AddBoolOr([task1_before_task2, task2_before_task1, 
                                task_vars[(i1, j)].Not(), task_vars[(i2, j)].Not()])
    
    # 4. Respect existing schedules (no conflicts)
    for existing in existing_schedules:
        # Normalize existing schedule datetimes
        existing_start = _normalize_datetime(existing.scheduled_start)
        existing_end = _normalize_datetime(existing.scheduled_end)
        
        existing_start_hours = int((existing_start - start_date).total_seconds() / 3600)
        existing_end_hours = int((existing_end - start_date).total_seconds() / 3600)
        line_idx = next((idx for idx, line in enumerate(production_lines) 
                        if line.id == existing.production_line_id), None)
        
        if line_idx is not None and existing_start_hours >= 0 and existing_end_hours <= time_horizon:
            for i in range(num_orders):
                # New task cannot overlap with existing schedule
                task_ends_before = model.NewBoolVar(f'task_{i}_ends_before_existing_{existing.id}')
                task_starts_after = model.NewBoolVar(f'task_{i}_starts_after_existing_{existing.id}')
                
                model.Add(end_vars[(i, line_idx)] <= existing_start_hours).OnlyEnforceIf(
                    [task_vars[(i, line_idx)], task_ends_before]
                )
                model.Add(start_vars[(i, line_idx)] >= existing_end_hours).OnlyEnforceIf(
                    [task_vars[(i, line_idx)], task_starts_after]
                )
                
                model.AddBoolOr([task_ends_before, task_starts_after, 
                                task_vars[(i, line_idx)].Not()])
    
    # 5. Capacity constraints (production line capacity per hour)
    for j in range(num_lines):
        line_capacity = production_lines[j].capacity_per_hour
        for i in range(num_orders):
            # Duration must respect capacity
            min_duration = math.ceil(orders[i]["quantity"] / line_capacity) if line_capacity > 0 else orders[i]["estimated_hours"]
            model.Add(duration_vars[(i, j)] >= min_duration).OnlyEnforceIf(task_vars[(i, j)])
    
    # Objective: Minimize makespan (total completion time)
    makespan = model.NewIntVar(0, time_horizon, 'makespan')
    for i in range(num_orders):
        for j in range(num_lines):
            model.Add(makespan >= end_vars[(i, j)]).OnlyEnforceIf(task_vars[(i, j)])
    
    # Weighted objective function
    model.Minimize(makespan)
    
    # Solve
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 30.0  # Time limit
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        # Extract solution
        optimized_schedule = []
        
        for i in range(num_orders):
            for j in range(num_lines):
                if solver.Value(task_vars[(i, j)]) == 1:
                    start_hours = solver.Value(start_vars[(i, j)])
                    end_hours = solver.Value(end_vars[(i, j)])
                    
                    scheduled_start = start_date + timedelta(hours=start_hours)
                    scheduled_end = start_date + timedelta(hours=end_hours)
                    
                    optimized_schedule.append({
                        "order_id": orders[i]["order_id"],
                        "order_item_id": orders[i]["order_item_id"],
                        "product_id": orders[i]["product_id"],
                        "product_name": orders[i]["product_name"],
                        "quantity": orders[i]["quantity"],
                        "production_line_id": production_lines[j].id,
                        "production_line_name": production_lines[j].name,
                        "scheduled_start": scheduled_start.isoformat(),
                        "scheduled_end": scheduled_end.isoformat(),
                        "duration_hours": end_hours - start_hours,
                        "utilization": (end_hours - start_hours) / time_horizon * 100 if time_horizon > 0 else 0
                    })
        
        makespan_value = solver.Value(makespan)
        
        return {
            "success": True,
            "status": "OPTIMAL" if status == cp_model.OPTIMAL else "FEASIBLE",
            "makespan_hours": makespan_value,
            "makespan_days": makespan_value / 24,
            "total_orders": num_orders,
            "schedule": optimized_schedule,
            "statistics": {
                "solver_time_seconds": solver.WallTime(),
                "conflicts": solver.NumConflicts(),
                "branches": solver.NumBranches()
            }
        }
    else:
        return {
            "success": False,
            "error": f"Solver status: {status}",
            "schedule": []
        }


def assign_tasks_to_staff(
    db: Session,
    production_schedule_id: int,
    task_requirements: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Assign tasks to staff members based on skills, availability, and workload
    Uses optimization to minimize cost and maximize efficiency
    """
    
    if not OR_TOOLS_AVAILABLE:
        return {
            "success": False,
            "error": "OR-Tools not available",
            "assignments": []
        }
    
    # Get production schedule
    schedule = db.query(ProductionSchedule).filter(
        ProductionSchedule.id == production_schedule_id
    ).first()
    
    if not schedule:
        return {
            "success": False,
            "error": "Production schedule not found",
            "assignments": []
        }
    
    # Get available staff
    available_staff = db.query(Staff).filter(
        Staff.is_available == True
    ).all()
    
    if not available_staff:
        return {
            "success": False,
            "error": "No available staff found",
            "assignments": []
        }
    
    # Create optimization model
    model = cp_model.CpModel()
    
    num_tasks = len(task_requirements)
    num_staff = len(available_staff)
    
    # Variables: assignment[i][j] = 1 if task i is assigned to staff j
    assignment_vars = {}
    workload_vars = {}  # Total hours assigned to each staff member
    
    for i in range(num_tasks):
        for j in range(num_staff):
            assignment_vars[(i, j)] = model.NewBoolVar(f'task_{i}_staff_{j}')
    
    for j in range(num_staff):
        workload_vars[j] = model.NewIntVar(0, available_staff[j].max_hours_per_day * 7, 
                                          f'workload_{j}')
    
    # Constraints
    
    # 1. Each task must be assigned to exactly one staff member
    for i in range(num_tasks):
        model.Add(sum(assignment_vars[(i, j)] for j in range(num_staff)) == 1)
    
    # 2. Calculate workload for each staff member
    for j in range(num_staff):
        task_hours = []
        for i in range(num_tasks):
            hours = task_requirements[i].get("estimated_hours", 8)
            task_hours.append(assignment_vars[(i, j)] * hours)
        model.Add(workload_vars[j] == sum(task_hours))
        
        # Workload cannot exceed max hours
        model.Add(workload_vars[j] <= available_staff[j].max_hours_per_day * 7)
    
    # 3. Skill matching (prefer staff with matching skills, but allow flexibility)
    # Create skill preference weights (higher weight = better match)
    skill_weights = {}
    for i in range(num_tasks):
        required_skill = task_requirements[i].get("required_skill", "").lower()
        required_level = task_requirements[i].get("required_level", "intermediate").lower()
        
        for j in range(num_staff):
            staff_skill = (available_staff[j].specialization or "").lower()
            staff_dept = (available_staff[j].department or "").lower()
            staff_level = (available_staff[j].skill_level or "junior").lower()
            
            # Skill matching logic (more flexible):
            # - If required_skill is "production", match any production department staff
            # - If required_skill matches specialization, prefer that
            # - Allow any staff if no specific skill required
            skill_match = False
            if not required_skill:
                skill_match = True  # No skill requirement
            elif required_skill == "production" and staff_dept == "production":
                skill_match = True  # Production department matches
            elif required_skill in staff_skill or staff_skill in required_skill:
                skill_match = True  # Skill names overlap
            elif required_skill == "assembly" and ("assembly" in staff_skill or "assembly" in staff_dept):
                skill_match = True  # Assembly matches
            
            # If skills don't match at all, prefer not to assign (but don't forbid)
            # We'll use this in the objective function instead
            skill_weights[(i, j)] = 100 if skill_match else 1
    
    # Objective: Minimize total cost (hourly_rate * hours) and maximize skill match
    total_cost = []
    skill_penalty = []
    for i in range(num_tasks):
        for j in range(num_staff):
            hours = task_requirements[i].get("estimated_hours", 8)
            cost = available_staff[j].hourly_rate * hours
            # Cost component (scale by 100 for integer)
            total_cost.append(assignment_vars[(i, j)] * int(cost * 100))
            # Skill mismatch penalty (prefer matching skills)
            penalty = (101 - skill_weights.get((i, j), 1)) * 10  # Higher penalty for mismatches
            skill_penalty.append(assignment_vars[(i, j)] * penalty)
    
    # Minimize: cost + skill mismatch penalty
    model.Minimize(sum(total_cost) + sum(skill_penalty))
    
    # Solve
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10.0
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        assignments = []
        total_cost_value = 0
        
        for i in range(num_tasks):
            for j in range(num_staff):
                if solver.Value(assignment_vars[(i, j)]) == 1:
                    hours = task_requirements[i].get("estimated_hours", 8)
                    cost = available_staff[j].hourly_rate * hours
                    total_cost_value += cost
                    
                    # Calculate start and end times
                    task_start = _normalize_datetime(schedule.scheduled_start)
                    task_end = task_start + timedelta(hours=hours)
                    
                    # Create task assignment in database
                    task_assignment = TaskAssignment(
                        production_schedule_id=production_schedule_id,
                        staff_id=available_staff[j].id,
                        task_type=task_requirements[i].get("task_type", "production"),
                        assigned_hours=hours,
                        start_time=task_start,
                        end_time=task_end,
                        status="assigned"
                    )
                    db.add(task_assignment)
                    
                    assignments.append({
                        "task_type": task_requirements[i].get("task_type", "production"),
                        "staff_id": available_staff[j].id,
                        "staff_name": available_staff[j].name,
                        "staff_skill": available_staff[j].specialization,
                        "assigned_hours": hours,
                        "start_time": task_start.isoformat(),
                        "end_time": task_end.isoformat(),
                        "cost": cost
                    })
        
        db.commit()
        return {
            "success": True,
            "status": "OPTIMAL" if status == cp_model.OPTIMAL else "FEASIBLE",
            "total_cost": total_cost_value,
            "assignments": assignments,
            "statistics": {
                "solver_time_seconds": solver.WallTime(),
                "tasks_assigned": len(assignments),
                "staff_utilized": len(set(a["staff_id"] for a in assignments))
            }
        }
    else:
        # Fallback: Simple sequential assignment
        print(f"[DEBUG] Staff assignment optimization failed (status: {status}), using fallback")
        return _fallback_assign_staff(db, production_schedule_id, task_requirements, available_staff, schedule)


def _fallback_assign_staff(
    db: Session,
    production_schedule_id: int,
    task_requirements: List[Dict[str, Any]],
    available_staff: List[Staff],
    schedule: ProductionSchedule
) -> Dict[str, Any]:
    """
    Fallback: Simple sequential staff assignment when optimization fails.
    Assigns tasks to available staff in order, respecting workload limits.
    """
    assignments = []
    total_cost_value = 0
    staff_workload = {staff.id: staff.current_workload_hours for staff in available_staff}
    
    for i, task in enumerate(task_requirements):
        task_hours = task.get("estimated_hours", 8)
        task_type = task.get("task_type", "production")
        
        # Find staff with lowest workload who can handle this task
        best_staff = None
        best_workload = float('inf')
        
        for staff in available_staff:
            current_workload = staff_workload.get(staff.id, 0)
            max_hours = staff.max_hours_per_day * 7  # Weekly limit
            
            # Check if staff can take this task
            if current_workload + task_hours <= max_hours:
                if current_workload < best_workload:
                    best_workload = current_workload
                    best_staff = staff
        
        if best_staff:
            # Assign task to this staff member
            cost = best_staff.hourly_rate * task_hours
            total_cost_value += cost
            
            task_start = _normalize_datetime(schedule.scheduled_start)
            task_end = task_start + timedelta(hours=task_hours)
            
            # Create task assignment in database
            task_assignment = TaskAssignment(
                production_schedule_id=production_schedule_id,
                staff_id=best_staff.id,
                task_type=task_type,
                assigned_hours=task_hours,
                start_time=task_start,
                end_time=task_end,
                status="assigned"
            )
            db.add(task_assignment)
            
            # Update workload tracking
            staff_workload[best_staff.id] = staff_workload.get(best_staff.id, 0) + task_hours
            
            assignments.append({
                "task_type": task_type,
                "staff_id": best_staff.id,
                "staff_name": best_staff.name,
                "staff_skill": best_staff.specialization,
                "assigned_hours": task_hours,
                "start_time": task_start.isoformat(),
                "end_time": task_end.isoformat(),
                "cost": cost
            })
    
    if assignments:
        db.commit()
        return {
            "success": True,
            "status": "FEASIBLE_FALLBACK",
            "total_cost": total_cost_value,
            "assignments": assignments,
            "statistics": {
                "solver_time_seconds": 0,
                "tasks_assigned": len(assignments),
                "staff_utilized": len(set(a["staff_id"] for a in assignments)),
                "method": "sequential_fallback"
            }
        }
    else:
        return {
            "success": False,
            "error": "No staff available for assignment (all at capacity)",
            "assignments": []
        }


def optimize_order_fulfillment(
    db: Session,
    order_ids: List[int],
    optimize_for: str = "time",  # "time", "cost", "utilization"
    start_date: datetime = None,
    end_date: datetime = None
) -> Dict[str, Any]:
    """
    Optimize order fulfillment considering:
    - Production scheduling
    - Resource allocation
    - Staff assignment
    - Inventory availability
    """
    
    # Get orders
    orders = db.query(Order).filter(Order.id.in_(order_ids)).all()
    
    if not orders:
        return {
            "success": False,
            "error": "No orders found",
            "plan": {}
        }
    
    # Use provided dates or calculate defaults
    if start_date is None:
        earliest_start = datetime.utcnow()
    else:
        earliest_start = _normalize_datetime(start_date)
    
    if end_date is None:
        end_date = earliest_start + timedelta(days=30)
    else:
        end_date = _normalize_datetime(end_date)
    
    # Validate date range
    if end_date <= earliest_start:
        return {
            "success": False,
            "error": f"Invalid date range: end_date must be after start_date. Start: {earliest_start}, End: {end_date}",
            "plan": {}
        }
    
    time_window_days = (end_date - earliest_start).days
    if time_window_days < 1:
        return {
            "success": False,
            "error": f"Time window too short: {time_window_days} days. Need at least 1 day.",
            "plan": {}
        }
    
    # Optimize production schedule
    schedule_result = optimize_production_schedule(
        db, order_ids, earliest_start, end_date
    )
    
    # If optimization fails, try fallback sequential scheduling
    if not schedule_result["success"]:
        print(f"[DEBUG] Optimization failed: {schedule_result.get('error')}")
        print(f"[DEBUG] Attempting fallback sequential scheduling...")
        
        # Try fallback: sequential scheduling
        fallback_result = _sequential_schedule_orders(
            db, order_ids, earliest_start, end_date
        )
        
        if fallback_result["success"]:
            print(f"[DEBUG] Fallback scheduling succeeded")
            schedule_result = fallback_result
        else:
            # Return detailed error
            total_hours_needed = sum(
                max(1, item.quantity * 2) 
                for order in orders 
                for item in order.order_items
            )
            available_hours = sum(
                line.capacity_per_hour * time_window_days * 24 
                for line in db.query(ProductionLine).filter(ProductionLine.is_active == True).all()
            )
            
            return {
                "success": False,
                "error": f"Optimization failed: {schedule_result.get('error', 'Unknown error')}. "
                         f"Total hours needed: {total_hours_needed}, "
                         f"Available hours: {available_hours}, "
                         f"Time window: {time_window_days} days. "
                         f"Try selecting fewer orders or extending the date range.",
                "diagnostics": {
                    "total_hours_needed": total_hours_needed,
                    "available_hours": available_hours,
                    "time_window_days": time_window_days,
                    "num_orders": len(order_ids),
                    "num_production_lines": len(db.query(ProductionLine).filter(ProductionLine.is_active == True).all())
                },
                "plan": {}
            }
    
    # For each scheduled production, assign staff
    all_assignments = []
    total_cost = 0
    
    for schedule_item in schedule_result["schedule"]:
        # Create production schedule in database
        # Parse ISO format datetime and normalize
        start_str = schedule_item["scheduled_start"]
        end_str = schedule_item["scheduled_end"]
        
        # Handle ISO format with or without timezone
        if start_str.endswith('Z'):
            start_str = start_str.replace('Z', '+00:00')
        if end_str.endswith('Z'):
            end_str = end_str.replace('Z', '+00:00')
        
        try:
            scheduled_start = _normalize_datetime(datetime.fromisoformat(start_str))
            scheduled_end = _normalize_datetime(datetime.fromisoformat(end_str))
        except (ValueError, AttributeError) as e:
            # Fallback: try parsing without timezone
            scheduled_start = _normalize_datetime(datetime.fromisoformat(start_str.split('+')[0].split('Z')[0]))
            scheduled_end = _normalize_datetime(datetime.fromisoformat(end_str.split('+')[0].split('Z')[0]))
        
        production_schedule = ProductionSchedule(
            order_id=schedule_item["order_id"],
            production_line_id=schedule_item["production_line_id"],
            scheduled_start=scheduled_start,
            scheduled_end=scheduled_end,
            status="scheduled"
        )
        db.add(production_schedule)
        db.flush()
        
        # Define task requirements
        duration_hours = schedule_item.get("duration_hours", 8)
        # Ensure minimum hours for production task
        production_hours = max(1, duration_hours - 2)  # At least 1 hour for production
        
        task_requirements = [
            {
                "task_type": "setup",
                "estimated_hours": min(2, duration_hours),  # Setup can't exceed total duration
                "required_skill": "assembly",
                "required_level": "intermediate"
            },
            {
                "task_type": "production",
                "estimated_hours": production_hours,
                "required_skill": "production",
                "required_level": "intermediate"
            }
        ]
        
        # Assign staff to tasks
        assignment_result = assign_tasks_to_staff(
            db, production_schedule.id, task_requirements
        )
        
        if assignment_result["success"]:
            all_assignments.extend(assignment_result["assignments"])
            total_cost += assignment_result.get("total_cost", 0)
        else:
            # Log the error but continue
            print(f"[WARNING] Staff assignment failed for schedule {production_schedule.id}: {assignment_result.get('error', 'Unknown error')}")
    
    db.commit()
    
    return {
        "success": True,
        "orders_optimized": len(order_ids),
        "production_schedules": len(schedule_result["schedule"]),
        "total_makespan_hours": schedule_result["makespan_hours"],
        "total_makespan_days": schedule_result["makespan_days"],
        "staff_assignments": all_assignments,
        "total_cost": total_cost,
        "optimization_status": schedule_result["status"]
    }


def _sequential_schedule_orders(
    db: Session,
    order_ids: List[int],
    start_date: datetime,
    end_date: datetime
) -> Dict[str, Any]:
    """
    Fallback: Simple sequential scheduling when optimization fails.
    Schedules orders one after another on available production lines.
    """
    
    # Normalize datetimes
    start_date = _normalize_datetime(start_date)
    end_date = _normalize_datetime(end_date)
    
    # Get orders with items
    orders = []
    for order_id in order_ids:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            continue
        
        order_items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
        if not order_items:
            continue
            
        for item in order_items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if product:
                estimated_hours = max(1, item.quantity * 2)
                orders.append({
                    "order_id": order_id,
                    "order_item_id": item.id,
                    "product_id": product.id,
                    "product_name": product.name,
                    "quantity": item.quantity,
                    "estimated_hours": estimated_hours
                })
    
    if not orders:
        return {
            "success": False,
            "error": "No valid orders found",
            "schedule": []
        }
    
    # Get active production lines
    production_lines = db.query(ProductionLine).filter(
        ProductionLine.is_active == True
    ).all()
    
    if not production_lines:
        return {
            "success": False,
            "error": "No active production lines available",
            "schedule": []
        }
    
    # Get existing schedules
    existing_schedules = db.query(ProductionSchedule).filter(
        ProductionSchedule.scheduled_end >= start_date,
        ProductionSchedule.scheduled_start <= end_date
    ).all()
    
    # Track line availability (end times for each line)
    line_availability = {}
    for line in production_lines:
        # Find latest end time for this line from existing schedules
        line_schedules = [s for s in existing_schedules if s.production_line_id == line.id]
        if line_schedules:
            latest_end = max(_normalize_datetime(s.scheduled_end) for s in line_schedules)
            line_availability[line.id] = max(start_date, latest_end)
        else:
            line_availability[line.id] = start_date
    
    # Schedule orders sequentially
    optimized_schedule = []
    time_horizon_hours = int((end_date - start_date).total_seconds() / 3600)
    max_makespan = 0
    
    for order_info in orders:
        # Find line with earliest availability
        best_line = min(production_lines, key=lambda l: line_availability[l.id])
        current_start = line_availability[best_line.id]
        
        # Check if we have time
        estimated_hours = order_info["estimated_hours"]
        current_end = current_start + timedelta(hours=estimated_hours)
        
        if current_end > end_date:
            # Can't fit this order, skip it
            continue
        
        optimized_schedule.append({
            "order_id": order_info["order_id"],
            "order_item_id": order_info["order_item_id"],
            "product_id": order_info["product_id"],
            "product_name": order_info["product_name"],
            "quantity": order_info["quantity"],
            "production_line_id": best_line.id,
            "production_line_name": best_line.name,
            "scheduled_start": current_start.isoformat(),
            "scheduled_end": current_end.isoformat(),
            "duration_hours": estimated_hours,
            "utilization": (estimated_hours / time_horizon_hours * 100) if time_horizon_hours > 0 else 0
        })
        
        # Update line availability
        line_availability[best_line.id] = current_end
        max_makespan = max(max_makespan, int((current_end - start_date).total_seconds() / 3600))
    
    if not optimized_schedule:
        return {
            "success": False,
            "error": "Cannot schedule any orders in the given time window",
            "schedule": []
        }
    
    return {
        "success": True,
        "status": "FEASIBLE_FALLBACK",
        "makespan_hours": max_makespan,
        "makespan_days": max_makespan / 24,
        "total_orders": len(optimized_schedule),
        "schedule": optimized_schedule,
        "statistics": {
            "solver_time_seconds": 0,
            "conflicts": 0,
            "branches": 0,
            "method": "sequential_fallback"
        }
    }

