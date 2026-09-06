import time
from contextlib import contextmanager


@contextmanager
def timer(label: str):
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed_ms = (time.perf_counter() - start) * 1000
        print(f"{label}: {elapsed_ms:.2f}ms")


with timer("normalize tasks"):
    print("something")
    # normilized = [t["title"].strip().title() for t in raw_tasks]
