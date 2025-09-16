#!/usr/bin/env python3
"""
Simple log parsing helpers (stub).
You can extend this to parse sensor logs, extract timestamps, and plot.
"""

import argparse
import re
from pathlib import Path

def extract_distances(log_file):
    pattern = re.compile(r"Distance: (\d+\.\d+|None) m")
    distances = []
    for line in Path(log_file).read_text().splitlines():
        m = pattern.search(line)
        if m:
            v = m.group(1)
            distances.append(None if v == "None" else float(v))
    return distances

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("logfile")
    args = parser.parse_args()
    d = extract_distances(args.logfile)
    print("Distances found:", len(d))
    print(d[:20])

if __name__ == "__main__":
    main()
