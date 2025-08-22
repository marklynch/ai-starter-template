from setuptools import setup, find_packages

setup(
    name="langchain-testing",
    version="0.1.0",
    description="LangChain testing environment",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        # Requirements will be installed from requirements.txt
    ],
    extras_require={
        "dev": [
            "pytest>=8.3.0",
            "pytest-asyncio>=0.24.0",
            "black>=24.8.0",
            "isort>=5.13.0",
            "mypy>=1.11.0",
            "ruff>=0.6.0",
        ]
    },
)