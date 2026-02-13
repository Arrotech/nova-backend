from typing import Optional
from sqlalchemy.orm import Session
from app.services.base import CRUDBase
from app.models.site import SiteContent
from app.schemas.site import SiteContentCreate, SiteContentUpdate

class CRUDSiteContent(CRUDBase[SiteContent, SiteContentCreate, SiteContentUpdate]):
    def get_by_key(self, db: Session, key: str) -> Optional[SiteContent]:
        return db.query(self.model).filter(self.model.key == key).first()

site_content = CRUDSiteContent(SiteContent)
