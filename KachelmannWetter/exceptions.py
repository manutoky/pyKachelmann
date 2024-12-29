"""KachelmannWetter exceptions."""

class KachelmannWetterError(Exception):
    """Base class for KachelmannWetter errors."""

    def __init__(self, status: str) -> None:
        """Initialize."""
        super().__init__(status)
        self.status = status


class ApiError(KachelmannWetterError):
    """Raised when AccuWeather API request ended in error."""


class InvalidApiKeyError(KachelmannWetterError):
    """Raised when API Key format is invalid."""


class InvalidCoordinatesError(KachelmannWetterError):
    """Raised when coordinates are invalid."""
