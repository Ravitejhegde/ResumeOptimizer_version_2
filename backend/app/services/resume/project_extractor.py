import re


class ProjectExtractor:

    @staticmethod
    def extract(text: str) -> list[str]:

        projects = []

        pattern = re.compile(
            r"(project[s]?:?\s*)(.*)",
            re.IGNORECASE,
        )

        for line in text.splitlines():

            match = pattern.search(line)

            if match:

                projects.append(
                    match.group(2).strip()
                )

        return projects