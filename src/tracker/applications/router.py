from fastapi import APIRouter, Depends, Request

from tracker.applications.service import ApplicationsService
from tracker.applications.dependencies import get_applications_service
from tracker.applications.schema import ApplicationCreate, ApplicationUpdate, ApplicationStatusUpdate
from tracker.applications.models import ApplicationStatus


router = APIRouter(
    prefix="/applications/api/v1",
    tags=["Applications"],
    dependencies=[]
)


@router.post("/", status_code=201)
async def create_application(
    request: Request,
    data: ApplicationCreate,
    service: ApplicationsService = Depends(get_applications_service),
):
    await service.create_job_application(data)
    return {"msg": "Job application created"}, 201



@router.patch("/{id}", status_code=200)
async def update_application(
    id,
    request: Request,
    data: ApplicationUpdate,
    service: ApplicationsService = Depends(get_applications_service),
):
    await service.update_job_application(id, data)
    return {"msg": "Job application updated"}, 200


@router.delete("/{id}", status_code=200)
async def delete_application(
    id,
    request: Request,
    service: ApplicationsService = Depends(get_applications_service),
):
    data: ApplicationStatusUpdate = {"status": ApplicationStatus.DELETED }
    await service.update_job_application(id, data)
    return {"msg": "Job application updated"}, 200