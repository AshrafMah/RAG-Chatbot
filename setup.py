from setuptools import setup, find_packages

setup(
    name="swift",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "weaviate-client",
        "python-dotenv",
        "openai",
        "black",
        "wasabi",
        "typer",
        "haystack-ai",
        "nltk",
        "fastapi",
        "uvicorn",
        "pytest",
        "mypy",
    ],
)