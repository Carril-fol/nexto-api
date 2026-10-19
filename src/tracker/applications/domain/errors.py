from uuid import UUID

from tracker.shared.errors import DomainError


class ApplicationNotFound(DomainError):
    def __init__(self, application_id: UUID) -> None:
        self.application_id = application_id
        super().__init__(f"Postulación {application_id} no encontrada")


class InvalidStatusTransition(DomainError):
    def __init__(self, current: str, requested: str) -> None:
        self.current = current
        self.requested = requested
        super().__init__(f"Transición no permitida: {current} → {requested}")


class InvalidJobLink(DomainError):
    def __init__(self, link: str) -> None:
        self.link = link
        super().__init__(f"Link inválido: {link}")