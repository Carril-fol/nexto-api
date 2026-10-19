from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4, UUID

from tracker.applications.domain.errors import InvalidStatusTransition, InvalidJobLink

_ALLOWED = {
    "applied":   {"interview", "rejected", "withdrawn"},
    "interview": {"offer", "rejected", "withdrawn"},
    "offer":     {"withdrawn"},
    "rejected":  set(),
    "withdrawn": set(),
}

@dataclass
class JobApplication:
    id: UUID
    position: str
    link: str
    description: str
    cv_id: UUID
    status: str
    created_at: datetime

    @classmethod
    def create(cls, position: str, link: str, description: str, cv_id: UUID) -> "JobApplication":
        position = position.strip()
        if not link.startswith(("http://", "https://")):
            raise InvalidJobLink(link)
        return cls(
            id=uuid4(),
            position=position,
            link=link,
            description=description,
            cv_id=cv_id,
            status="applied",
            created_at=datetime.now(timezone.utc),
        )

    def change_status(self, new_status: str) -> None:
        if new_status not in _ALLOWED[self.status]:
            raise InvalidStatusTransition(self.status, new_status)
        self.status = new_status