from setuptools import setup, find_packages

setup(
    name="taskmaster-backend",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "sqlmodel==0.0.8",
        "uvicorn==0.24.0",
        "psycopg2-binary==2.9.9",
        "python-multipart==0.0.6",
        "pydantic==2.5.0",
        "pydantic-settings==2.1.0",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "neon==0.2.0",
        "jinja2==3.1.2",
        "python-dotenv==1.0.0",
        "asyncpg==0.29.0",
        "cryptography==41.0.8",
        "sqlalchemy==2.0.23"
    ],
    python_requires=">=3.8",
)