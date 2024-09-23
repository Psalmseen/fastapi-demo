from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from core.config.database import SessionLocal, engine
from app.models import organizationModel
from app.shemas import organizationSchema
from app.service import organizationService

organizationModel.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/organization', response_model= organizationSchema.Organization)
def create_organization(organization: organizationSchema.OrganizationBase, db:Session = Depends(get_db)):
    
    return organizationService.create_organization(db=db, organization=organization)


@app.get('/organization/{organizationId}', response_model=organizationSchema.Organization)
def get_organization(organizationId:int, db:Session = Depends(get_db)):
    return organizationService.get_organization(db=db, organization_id=organizationId)


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(app, host="0.0.0.0",port=9080)