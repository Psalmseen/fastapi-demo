from core.utils.utils import generate_random_uuid
from api.v1.app import organizationModel
from dto import organizationSchema
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


def create_organization(db:Session, organization:organizationSchema.OrganizationBase):
    reg_id = generate_random_uuid()
    print(reg_id)
    # try:
    db_organization = organizationModel.Organization(id=reg_id, name = organization.name, address= organization.address, companyRegId = organization.companyRegId)
    db.add(db_organization)
    db.commit()
    db.refresh(db_organization)
    return db_organization

    # except SQLAlchemyError as e:
       
    #     print(f"An error occurred while creating the organization: {str(e)}")
    #     raise
   

def get_organization(db:Session, organization_id:int):
    try:
        return db.query(organizationModel.Organization).filter(
            organizationModel.Organization.id == organization_id).first()
    
    except SQLAlchemyError as e:      
        print(f"An error occurred while creating the organization: {str(e)}")

    
    