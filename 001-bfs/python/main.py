from collections import deque
import sys

# Minimal, didactic BFS on an implicit complete binary tree.
# Nodes are 0..size-1; children are 2*i+1 and 2*i+2 if < size.

# 0.0290s or 29ms
# def bfs(size: int, target: int) -> bool:
#     # base case
#     if size == 0:
#         return False

#     # create queue, put root on it
#     q = deque()
#     q.append(0)

#     while len(q) > 0:
#         i = q.popleft()

#         # we found target
#         if i == target:
#             return True

#         # add leaf nodes to search queue
#         for leaf in [2*i + 1, 2*i + 2]:
#             if leaf <= size:
#                 q.append(leaf)
    
#     return False
    

# 0.0312s or 25ms
def bfs(size: int, target: int) -> bool:
    if size == 0:
        return False
    q = deque([0])  # start at root index 0
    while q:
        i = q.popleft()
        if i == target:
            return True
        l = 2 * i + 1
        r = 2 * i + 2
        if l < size:
            q.append(l)
        if r < size:
            q.append(r)
    return False


def main():
    # Args: <size> <target>, defaults: 100000, size-1
    size = 100_000
    target = size - 1
    if len(sys.argv) > 1:
        try:
            size = max(0, int(sys.argv[1]))
            target = size - 1
        except ValueError:
            pass
    if len(sys.argv) > 2:
        try:
            target = max(0, int(sys.argv[2]))
        except ValueError:
            pass
    print(f"found: {bfs(size, target)}")


if __name__ == "__main__":
    main()

