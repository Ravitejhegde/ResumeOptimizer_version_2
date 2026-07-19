from app.services.intelligence.models import SkillCategory


# =====================================================
# Technology Database
# =====================================================

TECHNOLOGY_CATEGORY: dict[str, SkillCategory] = {

    # -----------------------------
    # Programming Languages
    # -----------------------------
    "python": SkillCategory.PROGRAMMING,
    "java": SkillCategory.PROGRAMMING,
    "javascript": SkillCategory.PROGRAMMING,
    "typescript": SkillCategory.PROGRAMMING,
    "c": SkillCategory.PROGRAMMING,
    "c++": SkillCategory.PROGRAMMING,
    "c#": SkillCategory.PROGRAMMING,
    "go": SkillCategory.PROGRAMMING,
    "golang": SkillCategory.PROGRAMMING,
    "php": SkillCategory.PROGRAMMING,
    "ruby": SkillCategory.PROGRAMMING,
    "kotlin": SkillCategory.PROGRAMMING,
    "swift": SkillCategory.PROGRAMMING,
    "dart": SkillCategory.PROGRAMMING,

    # -----------------------------
    # Frontend
    # -----------------------------
    "html": SkillCategory.FRONTEND,
    "css": SkillCategory.FRONTEND,
    "bootstrap": SkillCategory.FRONTEND,
    "tailwind": SkillCategory.FRONTEND,
    "tailwind css": SkillCategory.FRONTEND,
    "react": SkillCategory.FRONTEND,
    "angular": SkillCategory.FRONTEND,
    "vue": SkillCategory.FRONTEND,
    "vue.js": SkillCategory.FRONTEND,
    "next.js": SkillCategory.FRONTEND,
    "nuxt": SkillCategory.FRONTEND,
    "astro": SkillCategory.FRONTEND,
    "vite": SkillCategory.FRONTEND,

    # -----------------------------
    # Backend
    # -----------------------------
    "node.js": SkillCategory.BACKEND,
    "nodejs": SkillCategory.BACKEND,
    "express": SkillCategory.BACKEND,
    "express.js": SkillCategory.BACKEND,
    "spring": SkillCategory.BACKEND,
    "spring boot": SkillCategory.BACKEND,
    "fastapi": SkillCategory.BACKEND,
    "django": SkillCategory.BACKEND,
    "flask": SkillCategory.BACKEND,
    "asp.net": SkillCategory.BACKEND,
    "nestjs": SkillCategory.BACKEND,
    "rest api": SkillCategory.BACKEND,
    "rest apis": SkillCategory.BACKEND,
    "graphql": SkillCategory.BACKEND,

    # -----------------------------
    # Database
    # -----------------------------
    "sql": SkillCategory.DATABASE,
    "mysql": SkillCategory.DATABASE,
    "postgresql": SkillCategory.DATABASE,
    "mongodb": SkillCategory.DATABASE,
    "firebase": SkillCategory.DATABASE,
    "sqlite": SkillCategory.DATABASE,
    "oracle": SkillCategory.DATABASE,
    "redis": SkillCategory.DATABASE,
    "nosql": SkillCategory.DATABASE,

    # -----------------------------
    # Frameworks
    # -----------------------------
    "tensorflow": SkillCategory.FRAMEWORK,
    "keras": SkillCategory.FRAMEWORK,
    "pytorch": SkillCategory.FRAMEWORK,
    "opencv": SkillCategory.FRAMEWORK,
    "yolo": SkillCategory.FRAMEWORK,
    "scikit-learn": SkillCategory.FRAMEWORK,
    "pandas": SkillCategory.FRAMEWORK,
    "numpy": SkillCategory.FRAMEWORK,

    # -----------------------------
    # Cloud
    # -----------------------------
    "aws": SkillCategory.CLOUD,
    "azure": SkillCategory.CLOUD,
    "gcp": SkillCategory.CLOUD,
    "google cloud": SkillCategory.CLOUD,

    # -----------------------------
    # DevOps
    # -----------------------------
    "docker": SkillCategory.DEVOPS,
    "kubernetes": SkillCategory.DEVOPS,
    "jenkins": SkillCategory.DEVOPS,
    "github actions": SkillCategory.DEVOPS,
    "ci/cd": SkillCategory.DEVOPS,

    # -----------------------------
    # Testing
    # -----------------------------
    "pytest": SkillCategory.TESTING,
    "junit": SkillCategory.TESTING,
    "selenium": SkillCategory.TESTING,
    "postman": SkillCategory.TESTING,

    # -----------------------------
    # Tools
    # -----------------------------
    "git": SkillCategory.TOOLS,
    "github": SkillCategory.TOOLS,
    "gitlab": SkillCategory.TOOLS,
    "swagger": SkillCategory.TOOLS,
    "jira": SkillCategory.TOOLS,

    # -----------------------------
    # Mobile
    # -----------------------------
    "flutter": SkillCategory.MOBILE,
    "android": SkillCategory.MOBILE,
    "ios": SkillCategory.MOBILE,
    "react native": SkillCategory.MOBILE,
}


# =====================================================
# Recruiter Priority
# =====================================================

CATEGORY_PRIORITY = {

    SkillCategory.PROGRAMMING: 100,

    SkillCategory.FRONTEND: 95,

    SkillCategory.BACKEND: 95,

    SkillCategory.DATABASE: 90,

    SkillCategory.FRAMEWORK: 80,

    SkillCategory.DEVOPS: 85,

    SkillCategory.CLOUD: 80,

    SkillCategory.TESTING: 75,

    SkillCategory.TOOLS: 70,

    SkillCategory.MOBILE: 70,

    SkillCategory.AI: 60,

    SkillCategory.SOFT: 50,

    SkillCategory.OTHER: 10,

}