
from enum import Enum


class SkillCategory(str, Enum):

    PROGRAMMING = "Programming Languages"

    FRONTEND = "Frontend Technologies"

    BACKEND = "Backend Technologies"

    DATABASE = "Databases"

    FRAMEWORK = "Frameworks"

    DEVOPS = "DevOps"

    CLOUD = "Cloud"

    TOOLS = "Tools & Platforms"

    TESTING = "Testing"

    MOBILE = "Mobile"

    AI = "Artificial Intelligence"

    SOFT = "Soft Skills"

    OTHER = "Other"


class SkillAction(str, Enum):

    KEEP = "KEEP"

    REMOVE = "REMOVE"

    ADD = "ADD"