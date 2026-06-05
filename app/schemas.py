from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal


class CustomerBase(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    notes: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    name: Optional[str] = None


class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class VehicleBase(BaseModel):
    make: str
    model: str
    year: int
    vin: Optional[str] = None
    license_plate: Optional[str] = None
    color: Optional[str] = None
    mileage: Optional[int] = None
    notes: Optional[str] = None


class VehicleCreate(VehicleBase):
    customer_id: int


class VehicleUpdate(VehicleBase):
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None


class VehicleResponse(VehicleBase):
    id: int
    customer_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class InspectionItemBase(BaseModel):
    category: str
    component: str
    condition: Optional[str] = None
    notes: Optional[str] = None
    recommended_action: Optional[str] = None
    urgency: Optional[str] = None
    estimated_cost: Optional[float] = 0


class InspectionItemCreate(InspectionItemBase):
    inspection_id: int


class InspectionItemResponse(InspectionItemBase):
    id: int
    inspection_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class InspectionBase(BaseModel):
    date: date
    mileage: Optional[int] = None
    notes: Optional[str] = None


class InspectionCreate(InspectionBase):
    vehicle_id: int
    items: List[InspectionItemCreate] = []


class InspectionResponse(InspectionBase):
    id: int
    vehicle_id: int
    created_at: datetime
    updated_at: datetime
    items: List[InspectionItemResponse] = []

    class Config:
        from_attributes = True


class RepairBase(BaseModel):
    description: Optional[str] = None
    parts_cost: float = 0
    labor_cost: float = 0
    labor_hours: float = 0
    notes: Optional[str] = None


class RepairCreate(RepairBase):
    inspection_item_id: int
    job_id: Optional[int] = None


class RepairUpdate(BaseModel):
    description: Optional[str] = None
    status: Optional[str] = None
    parts_cost: Optional[float] = None
    labor_cost: Optional[float] = None
    labor_hours: Optional[float] = None
    notes: Optional[str] = None
    completed_at: Optional[datetime] = None


class RepairResponse(RepairBase):
    id: int
    inspection_item_id: int
    job_id: Optional[int] = None
    status: str
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class JobBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    quoted_total: float = 0


class JobCreate(JobBase):
    customer_id: int
    vehicle_id: int
    status: str = "quoted"


class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    quoted_total: Optional[float] = None
    actual_total: Optional[float] = None
    tax_amount: Optional[float] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    paid_at: Optional[datetime] = None


class JobResponse(JobBase):
    id: int
    customer_id: int
    vehicle_id: int
    status: str
    actual_total: float
    tax_amount: float
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    paid_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    repairs: List[RepairResponse] = []
    payments: List["PaymentResponse"] = []

    class Config:
        from_attributes = True


class PaymentBase(BaseModel):
    amount: float
    method: Optional[str] = None
    date: date
    notes: Optional[str] = None


class PaymentCreate(PaymentBase):
    job_id: int


class PaymentResponse(PaymentBase):
    id: int
    job_id: int
    created_at: datetime

    class Config:
        from_attributes = True


JobResponse.model_rebuild()
