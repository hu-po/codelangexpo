import sys

# Minimal, didactic iterative DFS with an explicit stack on an implicit tree.
# Nodes are 0..size-1; children are 2*i+1 and 2*i+2 when < size.


def dfs(size: int, target: int) -> bool:
    if size == 0:
        return False
    st = [0]  # start with root
    while st:
        i = st.pop()
        if i == target:
            return True
        l = 2 * i + 1
        r = 2 * i + 2
        if r < size:
            st.append(r)  # push right first
        if l < size:
            st.append(l)  # then left
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
    print(f"found: {dfs(size, target)}")


if __name__ == "__main__":
    main()

