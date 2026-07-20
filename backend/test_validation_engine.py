from backend.app.services.validator.quality_gate import (
    ValidationEngine,
)

original = (
    "Developed REST APIs using Spring Boot."
)

optimized = (
    "Designed scalable REST APIs using Java Spring Boot Docker AWS Kubernetes."
)

valid, reason = ValidationEngine.validate(
    original,
    optimized,
)

print("=" * 60)

print("Valid :", valid)

print("Reason:", reason)