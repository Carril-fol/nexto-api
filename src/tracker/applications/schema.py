from pydantic import BaseModel, ConfigDict, HttpUrl, Field, field_serializer
from tracker.applications.models import ApplicationStatus



class ApplicationBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    position: str = Field(min_length=1, max_length=200)
    company: str | None = Field(default=None, max_length=200)
    link: HttpUrl
    description: str = ""

    @field_serializer("link")
    def serialize_link(self, link: HttpUrl):
        return str(link)
    

class ApplicationCreate(ApplicationBase):
    model_config = ConfigDict(from_attributes=True)


class ApplicationUpdate(ApplicationBase):
    model_config = ConfigDict(from_attributes=True)

    position: str | None = Field(default=None, min_length=1, max_length=200)
    company: str | None = Field(default=None, max_length=200)
    link: HttpUrl | None = None
    description: str | None = None
    status: ApplicationStatus


class ApplicationStatusUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: ApplicationStatus
