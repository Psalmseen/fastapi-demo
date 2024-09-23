from pydantic import BaseModel

class OrganizationBase(BaseModel):
    companyRegId:str
    name: str
    address: str

class Organization(OrganizationBase):
    id: int

    class Config:
        from_attributes = True