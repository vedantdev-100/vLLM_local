
from pathlib import Path


# All directories to create
DIRECTORIES = [
    "configs",

    "src/llm_service",
    "src/llm_service/api/routes",
    "src/llm_service/api/schemas",
    "src/llm_service/core",
    "src/llm_service/inference",
    "src/llm_service/models",
    "src/llm_service/rag",
    "src/llm_service/utils",

    "scripts",

    "tests/unit",
    "tests/integration",
    "tests/e2e",

    "data/raw",
    "data/processed",
    "data/sample",

    "models",
    "logs",

    "notebooks/experiments",

    "benchmarks/results",

    "deployment/docker",
    "deployment/systemd",

    "docs",
]


# All files to create
FILES = [
    "README.md",
    "LICENSE",
    ".gitignore",
    ".env.example",
    "pyproject.toml",
    "Makefile",
    "docker-compose.yml",

    # Config
    "configs/base.yaml",
    "configs/development.yaml",
    "configs/production.yaml",
    "configs/models.yaml",

    # API
    "src/llm_service/__init__.py",
    "src/llm_service/api/__init__.py",
    "src/llm_service/api/main.py",
    "src/llm_service/api/routes/health.py",
    "src/llm_service/api/routes/chat.py",
    "src/llm_service/api/routes/models.py",
    "src/llm_service/api/schemas/requests.py",
    "src/llm_service/api/schemas/responses.py",

    # Core
    "src/llm_service/core/config.py",
    "src/llm_service/core/logging.py",
    "src/llm_service/core/exceptions.py",

    # Inference
    "src/llm_service/inference/client.py",
    "src/llm_service/inference/service.py",
    "src/llm_service/inference/generation.py",

    # Models
    "src/llm_service/models/registry.py",
    "src/llm_service/models/metadata.py",

    # RAG
    "src/llm_service/rag/chunking.py",
    "src/llm_service/rag/embeddings.py",
    "src/llm_service/rag/retriever.py",
    "src/llm_service/rag/pipeline.py",

    # Utils
    "src/llm_service/utils/gpu.py",
    "src/llm_service/utils/helpers.py",

    # Scripts
    "scripts/download_model.py",
    "scripts/check_gpu.py",
    "scripts/benchmark.py",
    "scripts/health_check.py",

    # Test placeholders
    "tests/unit/.gitkeep",
    "tests/integration/.gitkeep",
    "tests/e2e/.gitkeep",

    # Data placeholders
    "data/raw/.gitkeep",
    "data/processed/.gitkeep",
    "data/sample/.gitkeep",

    # Other placeholders
    "models/.gitkeep",
    "logs/.gitkeep",
    "notebooks/experiments/.gitkeep",
    "benchmarks/results/.gitkeep",

    # Deployment
    "deployment/docker/Dockerfile",
    "deployment/docker/docker-entrypoint.sh",
    "deployment/systemd/vllm.service",

    # Documentation
    "docs/architecture.md",
    "docs/setup.md",
    "docs/inference.md",
    "docs/deployment.md",
    "docs/troubleshooting.md",
]


def create_structure():
    root = Path.cwd()

    print(f"\nCreating structure in:")
    print(f"{root}\n")

    # Create directories
    for directory in DIRECTORIES:
        path = root / directory
        path.mkdir(parents=True, exist_ok=True)
        print(f"[DIR]  {directory}")

    # Create files
    for file in FILES:
        path = root / file
        path.parent.mkdir(parents=True, exist_ok=True)

        if not path.exists():
            path.touch()
            print(f"[FILE] {file}")
        else:
            print(f"[SKIP] {file} already exists")

    print("\n========================================")
    print("Project structure created successfully!")
    print("========================================\n")


if __name__ == "__main__":
    create_structure()

