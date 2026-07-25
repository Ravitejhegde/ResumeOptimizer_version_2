from app.services.validator.layout_validator import (
    LayoutValidator,
)

original = (
    "Developed REST APIs using Spring Boot."
)

optimized = (
    "Designed scalable REST APIs using Java and Spring Boot."
)

valid, reason = LayoutValidator.validate(
    original,
    optimized,
)

print(valid)
print(reason)