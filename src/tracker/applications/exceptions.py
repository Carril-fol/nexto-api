from tracker.shared.errors import DomainError

class ApplicationNotExists(DomainError):
    status_code = 404
    detail = "Job application not found"


class ApplicationAlreadyHasThatStatus(DomainError):
    status_code = 304
    detail = "Job application not found"
