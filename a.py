import sys
from pathlib import Path
import math
import psutil
import time

def process_memory() -> int:
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)
    return memory_consumed

memory: int = process_memory()
print(memory)