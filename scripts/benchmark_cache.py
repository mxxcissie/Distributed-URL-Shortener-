import statistics
import time
import requests

BASE_URL = "http://127.0.0.1:8000"
ORIGINAL_URL = "https://www.google.com"
HIT_RUNS = 20

def create_short_url() -> str:
    resp = requests.post(
        f"{BASE_URL}/shorten",
        json={"original_url": ORIGINAL_URL},
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["short_code"]

def measure_once(url: str) -> float:
    start = time.perf_counter()
    resp = requests.get(url, allow_redirects=False, timeout=10)
    resp.raise_for_status()
    end = time.perf_counter()
    return (end - start) * 1000.0

def main() -> None:
    short_code = create_short_url()
    short_url = f"{BASE_URL}/{short_code}"

    miss_ms = measure_once(short_url)

    hit_results = []
    for _ in range(HIT_RUNS):
        hit_results.append(measure_once(short_url))

    avg_hit = statistics.mean(hit_results)
    min_hit = min(hit_results)
    max_hit = max(hit_results)

    print(f"Short URL: {short_url}")
    print(f"Cache miss latency: {miss_ms:.2f} ms")
    print(f"Cache hit avg latency over {HIT_RUNS} runs: {avg_hit:.2f} ms")
    print(f"Cache hit min latency: {min_hit:.2f} ms")
    print(f"Cache hit max latency: {max_hit:.2f} ms")

    if avg_hit > 0:
        print(f"Approx speedup (miss / avg hit): {miss_ms / avg_hit:.2f}x")

if __name__ == "__main__":
    main()