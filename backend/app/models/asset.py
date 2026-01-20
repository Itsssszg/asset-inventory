from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, func

from app.db.base import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    asset_tag = Column(String(64), unique=True, index=True)
    name = Column(String(255))
    category = Column(String(64), index=True)
    subcategory = Column(String(64), index=True)
    asset_type = Column(String(64), index=True)
    status = Column(String(64), default="active", index=True)

    location = Column(String(255), nullable=True)
    serial_number = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
