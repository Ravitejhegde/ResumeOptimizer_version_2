from .models import Usage


class UsageRepository:
    """
    Temporary in-memory repository.

    Replace with PostgreSQL later.
    """

    _storage: dict[str, Usage] = {}

    @classmethod
    def get(
        cls,
        identity_id: str,
    ) -> Usage | None:

        return cls._storage.get(identity_id)

    @classmethod
    def save(
        cls,
        usage: Usage,
    ) -> None:

        cls._storage[usage.identity_id] = usage