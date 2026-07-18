from app.services.optimizer.resume_optimizer_service import (
    ResumeOptimizerService,
)

service = ResumeOptimizerService()

output = service.optimize(
    "storage/temp/Ravitej_Hegde_Resume_Fullstack.docx",
    """
Java Backend Developer

Responsibilities:
• Design scalable backend services
• Develop REST APIs
• Work with Spring Boot
• Optimize SQL queries
• Participate in Agile ceremonies
• Collaborate with cross-functional teams

Requirements:
• 2+ years Java
• Spring Boot
• Microservices
• Docker
• Git
• MySQL
• AWS
• CI/CD
""",
)

print("=" * 60)
print("Generated:", output)