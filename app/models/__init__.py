from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text, Boolean, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class JobStatus(str, enum.Enum):
    QUOTED = "quoted"
    ACTIVE = "active"
    COMPLETED = "completed"
    PAID = "paid"
    UNPAID = "unpaid"


class RepairStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    DEFERRED = "deferred"  # for 6-month items


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String)
    email = Column(String)
    address = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    vehicles = relationship("Vehicle", back_populates="customer", cascade="all, delete-orphan")
    jobs = relationship("Job", back_populates="customer", cascade="all, delete-orphan")


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    vin = Column(String)
    license_plate = Column(String)
    color = Column(String)
    mileage = Column(Integer)
    notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    customer = relationship("Customer", back_populates="vehicles")
    inspections = relationship("Inspection", back_populates="vehicle", cascade="all, delete-orphan")
    jobs = relationship("Job", back_populates="vehicle", cascade="all, delete-orphan")


class Inspection(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False, server_default=func.now())
    mileage = Column(Integer)
    notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    vehicle = relationship("Vehicle", back_populates="inspections")
    items = relationship("InspectionItem", back_populates="inspection", cascade="all, delete-orphan")


class InspectionItem(Base):
    __tablename__ = "inspection_items"

    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id", ondelete="CASCADE"), nullable=False)
    category = Column(String, nullable=False)  # brakes, tires, fluids, suspension, lights, etc.
    component = Column(String, nullable=False)  # front brake pads, rear tires, etc.
    condition = Column(String)  # good, fair, poor, critical
    notes = Column(Text)
    recommended_action = Column(String)  # replace, repair, monitor, flush
    urgency = Column(String)  # immediate, soon, next_service, monitor
    estimated_cost = Column(Float, default=0)
    created_at = Column(DateTime, server_default=func.now())

    inspection = relationship("Inspection", back_populates="items")
    repairs = relationship("Repair", back_populates="inspection_item", cascade="all, delete-orphan")


class Repair(Base):
    __tablename__ = "repairs"

    id = Column(Integer, primary_key=True, index=True)
    inspection_item_id = Column(Integer, ForeignKey("inspection_items.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True)
    description = Column(Text)
    status = Column(Enum(RepairStatus), default=RepairStatus.PENDING)
    parts_cost = Column(Float, default=0)
    labor_cost = Column(Float, default=0)
    labor_hours = Column(Float, default=0)
    completed_at = Column(DateTime, nullable=True)
    notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    inspection_item = relationship("InspectionItem", back_populates="repairs")
    job = relationship("Job", back_populates="repairs")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(JobStatus), default=JobStatus.QUOTED)
    title = Column(String)
    description = Column(Text)
    quoted_total = Column(Float, default=0)
    actual_total = Column(Float, default=0)
    tax_amount = Column(Float, default=0)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    paid_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    customer = relationship("Customer", back_populates="jobs")
    vehicle = relationship("Vehicle", back_populates="jobs")
    repairs = relationship("Repair", back_populates="job", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="job", cascade="all, delete-orphan")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Float, nullable=False)
    method = Column(String)  # cash, card, check, transfer
    date = Column(Date, nullable=False, server_default=func.now())
    notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    job = relationship("Job", back_populates="payments")
