# app/services/intelligence/constants/role_weights.py

FULL_STACK = {
    "react": 100,
    "react.js": 100,
    "node": 100,
    "node.js": 100,
    "express": 95,
    "express.js": 95,
    "typescript": 90,
    "javascript": 90,
    "html": 80,
    "css": 80,
    "rest api": 95,
    "restful api": 95,
    "microservices": 85,
    "mongodb": 85,
    "mysql": 80,
    "postgresql": 80,
    "git": 70,
    "docker": 50,
    "aws": 40,
    "azure": 40,
}

BACKEND = {
    "python": 95,
    "java": 95,
    "c#": 85,
    "spring": 95,
    "spring boot": 100,
    "node.js": 95,
    "express": 90,
    "fastapi": 90,
    "django": 90,
    "flask": 85,
    "rest api": 95,
    "microservices": 90,
    "mysql": 80,
    "postgresql": 80,
    "mongodb": 75,
    "redis": 70,
}

FRONTEND = {
    "react": 100,
    "angular": 100,
    "vue": 95,
    "next.js": 95,
    "javascript": 95,
    "typescript": 95,
    "html": 90,
    "css": 90,
    "bootstrap": 75,
    "tailwind css": 80,
}

AI = {
    "machine learning": 100,
    "deep learning": 100,
    "computer vision": 95,
    "opencv": 95,
    "tensorflow": 100,
    "pytorch": 100,
    "yolo": 95,
    "nlp": 90,
    "scikit-learn": 95,
    "pandas": 80,
    "numpy": 80,
}

DEVOPS = {
    "docker": 100,
    "kubernetes": 100,
    "jenkins": 95,
    "terraform": 95,
    "ansible": 90,
    "aws": 95,
    "azure": 95,
    "gcp": 95,
    "ci/cd": 90,
    "github actions": 85,
}

ROLE_WEIGHTS = {
    "AI/ML Engineer": AI,
    "Frontend Developer": FRONTEND,
    "Backend Developer": BACKEND,
    "Full Stack Developer": FULL_STACK,
    "DevOps Engineer": DEVOPS,
}