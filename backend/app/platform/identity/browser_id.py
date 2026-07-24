import uuid


class BrowserID:

    COOKIE_NAME = "resumeoptimizer_guest"

    @staticmethod
    def generate() -> str:
        return str(uuid.uuid4())