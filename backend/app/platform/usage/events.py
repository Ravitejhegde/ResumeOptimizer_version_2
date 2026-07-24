from enum import Enum


class UsageEvent(str, Enum):

    UPLOAD = "upload"

    ANALYZE = "analyze"

    OPTIMIZE = "optimize"

    DOWNLOAD = "download"