class FikenError(Exception):
    """Base exception for Fiken API errors."""

    def __init__(self, message: str, status_code: int | None = None):
        self.status_code = status_code
        super().__init__(message)


class AuthError(FikenError):
    """401 Unauthorized."""


class ForbiddenError(FikenError):
    """403 Forbidden."""


class NotFoundError(FikenError):
    """404 Not Found."""


class ValidationError(FikenError):
    """400 Bad Request / validation failure."""


class RateLimitError(FikenError):
    """429 Too Many Requests."""


class ServerError(FikenError):
    """5xx Server Error."""


class CompanySlugRequiredError(FikenError):
    """Raised when no company slug is provided and no default is configured."""

    def __init__(self):
        super().__init__(
            "company_slug is required. Either pass it explicitly or set "
            "FIKEN_DEFAULT_COMPANY_SLUG in your .env file.",
            status_code=None,
        )
