#!/usr/bin/env python3
"""
Setup script for Realtor Agent.
© Shylow Thompson. LLC 2026 - All Rights Reserved
"""

from setuptools import setup, find_packages

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="realtor-agent",
    version="0.1.0",
    author="Realtor Agent Team",
    author_email="team@realtoragent.com",
    description="AI-powered real estate acquisition platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/realtor-agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.12",
    install_requires=[
        "PyYAML>=6.0",
        "requests>=2.31.0",
        "pandas>=2.1.0",
        "numpy>=1.24.0",
        "pytest>=7.4.0",
        "pytest-mock>=3.12.0",
        "pytest-cov>=4.1.0",
        "black>=23.0.0",
        "flake8>=6.0.0",
        "mypy>=1.5.0",
        "psycopg2-binary>=2.9.0",
        "SQLAlchemy>=2.0.0",
        "alembic>=1.12.0",
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "aiohttp>=3.9.0",
        "httpx>=0.25.0",
        "redis>=5.0.0",
        "celery>=5.3.0",
        "prometheus-client>=0.19.0",
        "structlog>=23.2.0",
        "bcrypt>=4.1.0",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.0",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "twilio>=8.2.0",
        "sendgrid>=6.10.0",
        "openpyxl>=3.1.0",
        "python-multipart>=0.0.6",
        "python-dotenv>=1.0.0",
        "schedule>=1.2.0",
        "tenacity>=8.2.0",
        "click>=8.1.0",
    ],
    extras_require={
        "dev": [
            "pre-commit>=3.5.0",
            "jupyter>=1.0.0",
        ],
        "test": [
            "pytest>=7.4.0",
            "pytest-mock>=3.12.0",
            "pytest-cov>=4.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "realtor-agent=realtor_agent.cli:cli",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)