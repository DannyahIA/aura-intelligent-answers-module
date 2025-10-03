"""Setup script for Aura IA module."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="aura-ia",
    version="0.1.0",
    author="Daniel Tavares",
    author_email="daniel@aura-project.com",
    description="The brain of Aura's automation for intelligent financial AI responses",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DannyahIA/aura-intelligent-answers-module",
    project_urls={
        "Bug Reports": "https://github.com/DannyahIA/aura-intelligent-answers-module/issues",
        "Source": "https://github.com/DannyahIA/aura-intelligent-answers-module",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "google-generativeai>=0.3.0",
        "openai>=1.0.0",
        "aiohttp>=3.9.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
        ],
    },
    keywords="ai artificial-intelligence financial-ai nlp chatbot alexa voice-assistant gemini gpt openai",
)
