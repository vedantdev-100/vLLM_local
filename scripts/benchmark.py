import asyncio
import statistics
import time

import aiohttp


URL = "http://localhost:8000/v1/chat/completions"
MODEL = "Qwen/Qwen2.5-1.5B-Instruct"

REQUESTS = 10


PAYLOAD = {
    "model": MODEL,
    "messages": [
        {
            "role": "user",
            "content": (
                "Explain how a transformer-based "
                "language model generates text."
            ),
        }
    ],
    "temperature": 0.2,
    "max_tokens": 200,
}


async def run_request(session):

    start = time.perf_counter()

    async with session.post(
        URL,
        json=PAYLOAD,
    ) as response:

        data = await response.json()

    latency = time.perf_counter() - start

    return latency, data


async def main():

    async with aiohttp.ClientSession() as session:

        results = await asyncio.gather(
            *[
                run_request(session)
                for _ in range(REQUESTS)
            ]
        )

    latencies = [result[0] for result in results]

    print("\nBenchmark Results")
    print("=================")
    print(f"Requests       : {REQUESTS}")
    print(f"Average latency: {statistics.mean(latencies):.3f}s")
    print(f"Min latency    : {min(latencies):.3f}s")
    print(f"Max latency    : {max(latencies):.3f}s")
    print(
        f"P95 latency    : "
        f"{sorted(latencies)[int(len(latencies) * 0.95) - 1]:.3f}s"
    )

    sample = results[0][1]

    print(
        f"Prompt tokens  : "
        f"{sample['usage']['prompt_tokens']}"
    )

    print(
        f"Output tokens  : "
        f"{sample['usage']['completion_tokens']}"
    )


if __name__ == "__main__":
    asyncio.run(main())