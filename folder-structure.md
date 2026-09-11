local-llm/
│
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── pyproject.toml
├── Makefile
├── docker-compose.yml
│
├── configs/
│   ├── base.yaml
│   ├── development.yaml
│   ├── production.yaml
│   └── models.yaml
│
├── src/
│   └── llm_service/
│       ├── __init__.py
│       │
│       ├── api/
│       │   ├── __init__.py
│       │   ├── main.py
│       │   ├── routes/
│       │   │   ├── health.py
│       │   │   ├── chat.py
│       │   │   └── models.py
│       │   └── schemas/
│       │       ├── requests.py
│       │       └── responses.py
│       │
│       ├── core/
│       │   ├── config.py
│       │   ├── logging.py
│       │   └── exceptions.py
│       │
│       ├── inference/
│       │   ├── client.py
│       │   ├── service.py
│       │   └── generation.py
│       │
│       ├── models/
│       │   ├── registry.py
│       │   └── metadata.py
│       │
│       ├── rag/
│       │   ├── chunking.py
│       │   ├── embeddings.py
│       │   ├── retriever.py
│       │   └── pipeline.py
│       │
│       └── utils/
│           ├── gpu.py
│           └── helpers.py
│
├── scripts/
│   ├── download_model.py
│   ├── check_gpu.py
│   ├── benchmark.py
│   └── health_check.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
│
├── models/
│   └── .gitkeep
│
├── logs/
│   └── .gitkeep
│
├── notebooks/
│   └── experiments/
│
├── benchmarks/
│   └── results/
│
├── deployment/
│   ├── docker/
│   │   ├── Dockerfile
│   │   └── docker-entrypoint.sh
│   └── systemd/
│       └── vllm.service
│
└── docs/
    ├── architecture.md
    ├── setup.md
    ├── inference.md
    ├── deployment.md
    └── troubleshooting.md




Windows
  ↓
WSL2 / Ubuntu 26.04       ✅
  ↓
x86_64                     ✅
  ↓
RTX 5060 Ti 16GB           ✅
  ↓
Python 3.12               ✅
  ↓
vllm-env     