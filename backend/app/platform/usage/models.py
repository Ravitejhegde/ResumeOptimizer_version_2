from dataclasses import dataclass
from datetime import datetime


@dataclass
class Usage:

    identity_id: str

    uploads: int = 0

    analyses: int = 0

    optimizations: int = 0

    downloads: int = 0

    created_at: datetime | None = None

    updated_at: datetime | None = None