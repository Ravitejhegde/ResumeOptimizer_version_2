from app.services.jd.jd_parser import (
    JDParser,
)

jd = """
Looking for Java Backend Developer.

Required:

Java

Spring Boot

MySQL

Docker

Git

AWS

CI/CD

REST APIs
"""

knowledge = JDParser.parse(jd)

print("=" * 60)

print(
    sorted(
        knowledge.required
    )
)