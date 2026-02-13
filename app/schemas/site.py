from pydantic import BaseModel

class SiteContentBase(BaseModel):
    key: str
    value: str

class SiteContentCreate(SiteContentBase):
    pass

class SiteContentUpdate(BaseModel):
    value: str

class SiteContent(SiteContentBase):
    id: int

    class Config:
        from_attributes = True
