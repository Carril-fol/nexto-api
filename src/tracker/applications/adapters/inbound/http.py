from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from tracker.applications.application.change_status import ChangeApplicationStatus
from tracker.applications.application.create_application import CreateApplication
from tracker.applications.application.list_applications import ListApplications
from tracker.composition import (
    get_change_status,
    get_create_application,
    get_list_applications,
)

router = APIRouter(prefix="/applications", tags=["applications"])


class CreateApplicationRequest(BaseModel):
    position: str = Field(min_length=1, max_length=200)
    link: HttpUrl
    description: str
    cv_id: UUID


class ChangeStatusRequest(BaseModel):
    status: str


class ApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    position: str
    link: str
    description: str
    cv_id: UUID
    status: str
    created_at: datetime


@router.post("", status_code=201, response_model=ApplicationResponse)
async def create_application(
    body: CreateApplicationRequest,
    use_case: CreateApplication = Depends(get_create_application),
):
    return await use_case.execute(
        position=body.position,
        link=str(body.link),
        description=body.description,
        cv_id=body.cv_id,
    )


@router.get("", response_model=list[ApplicationResponse])
async def list_applications(use_case: ListApplications = Depends(get_list_applications)):
    return await use_case.execute()


@router.patch("/{application_id}/status", response_model=ApplicationResponse)
async def change_status(
    application_id: UUID,
    body: ChangeStatusRequest,
    use_case: ChangeApplicationStatus = Depends(get_change_status),
):
    return await use_case.execute(application_id, body.status)