from setuptools import setup, find_packages

setup(
    name="physical-ai-api",
    version="1.0.0",
    description="FastAPI backend for Physical AI Textbook Platform",
    author="Your Name",
    author_email="you@example.com",
    packages=find_packages(),
    python_requires=">=3.12",
    install_requires=[
        "fastapi>=0.100.0",
        "uvicorn[standard]>=0.23.0",
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
        "asyncpg>=0.28.0",
        "qdrant-client>=1.7.0",
        "google-generativeai>=0.3.0",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "python-multipart>=0.0.6",
        "httpx>=0.25.0",
        "mangum>=0.17.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "ruff>=0.1.0",
            "black>=23.0.0",
            "mypy>=1.5.0",
        ]
    },
)