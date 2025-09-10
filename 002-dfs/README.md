# 002 — DFS (Depth-First Search)

Goal: Given a complete binary tree with nodes labeled `0..size-1`, use iterative DFS (stack) to determine whether `target` exists.

CLI
- Usage: `dfs <size> <target>` (both optional)
- Defaults: `size=100000`, `target=size-1`

Notes
- The tree is implicit. For node index `i`, children are `2*i+1` and `2*i+2` when `< size`.
- Implementations avoid recursion to keep stack usage deterministic and comparable across languages.

