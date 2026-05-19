from datetime import date
from sqlalchemy import (
    Column,
    Integer,
    String, 
    Float, 
    ForeignKey, 
    Date
)
from sqlalchemy.orm import declarative_base, relationship

# базовый класс для моделей
Base = declarative_base()

class Warehouse(Base):

    __tablename__ = "warehouse"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    capacity = Column(Float, nullable=False)

    # cascade="all, delete-orphan" удаляет грузы, если удален склад
    shipments = relationship(
        "Shipment", 
        back_populates="warehouse", 
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Warehouse(id={self.id}, name='{self.name}', capacity={self.capacity})>"


class Shipment(Base):
    __tablename__ = "shipment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tracking_number = Column(String, unique=True, nullable=False)
    weight = Column(Float, nullable=False)
    status = Column(String, nullable=False, default="на складе")
    warehouse_id = Column(Integer, ForeignKey("warehouse.id", ondelete="CASCADE"), nullable=False)

    # обратная связь со складом
    warehouse = relationship("Warehouse", back_populates="shipments")
    
    # Связь м:м через промежуточную таблицу
    drivers = relationship(
        "ShipmentDriver", 
        back_populates="shipment", 
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Shipment(id={self.id}, tracking='{self.tracking_number}', status='{self.status}')>"


class Driver(Base):

    __tablename__ = "driver"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    license_number = Column(String, unique=True, nullable=False)
    #phone_number = Column(String, nullable=True) 

    # Связь м:м через промежуточную таблицу
    shipments = relationship(
        "ShipmentDriver", 
        back_populates="driver", 
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Driver(id={self.id}, name='{self.name}', license='{self.license_number}')>"


class ShipmentDriver(Base):
    __tablename__ = "shipment_driver"

    id = Column(Integer, primary_key=True, autoincrement=True)
    shipment_id = Column(Integer, ForeignKey("shipment.id", ondelete="CASCADE"), nullable=False)
    driver_id = Column(Integer, ForeignKey("driver.id", ondelete="CASCADE"), nullable=False)
    delivery_date = Column(Date, nullable=False, default=date.today)

    shipment = relationship("Shipment", back_populates="drivers")
    driver = relationship("Driver", back_populates="shipments")

    def __repr__(self):
        return f"<ShipmentDriver(id={self.id}, shipment_id={self.shipment_id}, driver_id={self.driver_id})>"
