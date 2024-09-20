import random
from models import organizationModel
from Schema import organizationSchema
from sqlalchemy.orm import Session


def create_organization(db:Session, organization:organizationSchema.OrganizationBase):
    db_organization = organizationModel.Organization( id=random.randint(1, 2346534) , name = organization.name, address= organization.address, companyRegId = organization.companyRegId)
    db.add(db_organization)
    db.commit()
    db.refresh(db_organization)
    return db_organization

def get_organization(db:Session, organizationId:int):
    return db.query(organizationModel.Organization).filter(organizationModel.Organization.id == organizationId).first()