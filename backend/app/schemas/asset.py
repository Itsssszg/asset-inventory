from pydantic import BaseModel, ConfigDict


class AssetBase(BaseModel):
    asset_tag: str
    name: str
    asset_type: str
    status: str = "active"
    location: str | None = None
    serial_number: str | None = None


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    asset_tag: str | None = None
    name: str | None = None
    asset_type: str | None = None
    status: str | None = None
    location: str | None = None
    serial_number: str | None = None


class AssetOut(AssetBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
