# vLLM_local
Setting up the LLM locally using vLLm inference engine.


[12/9/2026]
- pip install pytest pytest-asyncio 
- PYTHONPATH=src pytest -v
- PYTHONPATH=src pytest -v tests/integration
- pip install aiohttp
- PYTHONPATH=src python scripts/benchmark.py


Benchmarking features V2:
    Concurrency: (1, 2, 4, 8, 16)
    (Prompt sizes,Short,Medium,Long)
    Metrics: (TTFT,E2E latency,tokens/sec,P50,P95,P99,GPU memory,GPU utilization)

Docker cmds:
    [build]
    docker build \
  -f deployment/docker/Dockerfile \
  -t local-llm-api .
    [run]
    docker run \
  --rm \
  -p 8080:8080 \
  --env-file .env \
  local-llm-api


