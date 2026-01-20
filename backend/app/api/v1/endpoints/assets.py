from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.asset import create_asset, delete_asset, get_asset, get_asset_by_tag, list_assets, update_asset
from app.db.deps import get_db
from app.schemas.asset import AssetCreate, AssetOut, AssetUpdate
from app.models.asset import Asset


router = APIRouter()


@router.get("/", response_model=list[AssetOut])
def read_assets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[AssetOut]:
    return list_assets(db, skip=skip, limit=limit)


@router.post("/", response_model=AssetOut, status_code=status.HTTP_201_CREATED)
def create_asset_endpoint(asset_in: AssetCreate, db: Session = Depends(get_db)) -> AssetOut:
    existing = get_asset_by_tag(db, asset_in.asset_tag)
    if existing is not None:
        raise HTTPException(status_code=409, detail="asset_tag already exists")
    return create_asset(db, asset_in)


@router.get("/{asset_id}", response_model=AssetOut)
def read_asset(asset_id: int, db: Session = Depends(get_db)) -> AssetOut:
    asset = get_asset(db, asset_id)
    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.put("/{asset_id}", response_model=AssetOut)
def update_asset_endpoint(asset_id: int, asset_in: AssetUpdate, db: Session = Depends(get_db)) -> AssetOut:
    asset = get_asset(db, asset_id)
    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    if asset_in.asset_tag is not None:
        existing = get_asset_by_tag(db, asset_in.asset_tag)
        if existing is not None and existing.id != asset.id:
            raise HTTPException(status_code=409, detail="asset_tag already exists")

    return update_asset(db, asset, asset_in)


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset_endpoint(asset_id: int, db: Session = Depends(get_db)) -> None:
    asset = get_asset(db, asset_id)
    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    delete_asset(db, asset)
    return None
