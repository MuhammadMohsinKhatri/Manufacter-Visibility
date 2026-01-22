"""
Schemas for Optimization and Resource Management
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class ProductionOptimizationRequest(BaseModel):
    order_ids: List[int]
    start_date: datetime
    end_date: datetime
    objectives: Optional[Dict[str, float]] = None  # Weighted objectives


class TaskRequirement(BaseModel):
    task_type: str  # setup, production, quality_check, maintenance
    estimated_hours: float
    required_skill: Optional[str] = None
    required_level: Optional[str] = None  # junior, intermediate, senior, expert


class StaffAssignmentRequest(BaseModel):
    production_schedule_id: int
    task_requirements: List[TaskRequirement]


class OrderFulfillmentOptimizationRequest(BaseModel):
    order_ids: List[int]
    optimize_for: str = "time"  # time, cost, utilization
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class StaffCreate(BaseModel):
    name: str
    employee_id: str
    department: str
    skill_level: str
    specialization: str
    hourly_rate: float = 0.0
    max_hours_per_day: int = 8
    is_available: bool = True


class StaffUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    skill_level: Optional[str] = None
    specialization: Optional[str] = None
    hourly_rate: Optional[float] = None
    max_hours_per_day: Optional[int] = None
    is_available: Optional[bool] = None
    current_workload_hours: Optional[float] = None


class StaffResponse(BaseModel):
    id: int
    name: str
    employee_id: str
    department: str
    skill_level: str
    specialization: str
    hourly_rate: float
    is_available: bool
    max_hours_per_day: int
    current_workload_hours: float
    
    class Config:
        from_attributes = True


class TaskAssignmentResponse(BaseModel):
    id: int
    production_schedule_id: int
    staff_id: int
    task_type: str
    assigned_hours: float
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: str
    
    class Config:
        from_attributes = True

