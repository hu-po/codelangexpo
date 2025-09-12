# CodeLangExpo

Compare syntax and performance across languages on simple LeetCode-style problems. Each problem lives in its own root-level directory with an independent implementation in Rust, Go, C++, and Python.

## How This Repo Is Organized
- Each problem has its own directory at the repo root (e.g., `001-bfs`, `002-dfs`).
- Inside each problem directory you’ll find subfolders for each language: `rust/`, `go/`, `cpp/`, `python/`.
- The problem’s description and any notes live in that problem’s `README.md`.

## Problems Index
- 001 — BFS (Breadth-First Search): `001-bfs/README.md`
- 002 — DFS (Depth-First Search): `002-dfs/README.md`
 - 003 — Binary Search: `003-binary-search/README.md`

## Benchmark Harness
- Script: `bench.py`
- Examples:
  - `python3 bench.py --problem 001-bfs --size 100000 --target 99999`
  - `python3 bench.py --problem 002-dfs --size 100000 --target 99999`
  - `python3 bench.py --problem 003-binary-search --size 100000 --target 99999`
- Behavior: 
  - Builds Rust, Go, and C++ (unless `--no-build`) and runs all four implementations.
  - Reports build status, run success, and wall time per language.
