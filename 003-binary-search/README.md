# 003 — Binary Search

Goal: Given a sorted implicit array with values `0..size-1`, use binary search to determine whether `target` exists.

CLI
- Usage: `bsearch <size> <target>` (both optional)
- Defaults: `size=100000`, `target=size-1`

Notes
- The array is implicit and sorted ascending: `arr[i] = i` for `0 <= i < size`.
- Binary search runs in O(log n) time and O(1) extra space.

