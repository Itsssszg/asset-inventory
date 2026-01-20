from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetUpdate


def get_asset(db: Session, asset_id: int) -> Asset | None:
    return db.query(Asset).filter(Asset.id == asset_id).first()


def get_asset_by_tag(db: Session, asset_tag: str) -> Asset | None:
    return db.query(Asset).filter(Asset.asset_tag == asset_tag).first()


def list_assets(db: Session, skip: int = 0, limit: int = 100) -> list[Asset]:
    return db.query(Asset).offset(skip).limit(limit).all()


def create_asset(db: Session, asset_in: AssetCreate) -> Asset:
    obj = Asset(**asset_in.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_asset(db: Session, asset: Asset, asset_in: AssetUpdate) -> Asset:
    data = asset_in.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(asset, k, v)
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


def delete_asset(db: Session, asset: Asset) -> None:
    db.delete(asset)
    db.commit()
