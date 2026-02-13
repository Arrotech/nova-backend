from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.site import SiteContent, SiteContentCreate, SiteContentUpdate
from app.services import site_content as site_service
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[SiteContent])
def read_site_content(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    return site_service.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=SiteContent)
def create_site_content(
    *,
    db: Session = Depends(deps.get_db),
    content_in: SiteContentCreate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    content = site_service.get_by_key(db, key=content_in.key)
    if content:
        raise HTTPException(status_code=400, detail="Content with this key already exists")
    content = site_service.create(db, obj_in=content_in)
    return content

@router.put("/{key}", response_model=SiteContent)
def update_site_content(
    *,
    db: Session = Depends(deps.get_db),
    key: str,
    content_in: SiteContentUpdate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    content = site_service.get_by_key(db, key=key)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    content = site_service.update(db, db_obj=content, obj_in=content_in)
    return content
