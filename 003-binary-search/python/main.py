import sys

# Minimal, didactic binary search over an implicit sorted array.
# The array is conceptual: arr[i] = i for 0 <= i < size.


def bsearch(size: int, target: int) -> bool:
    lo, hi = 0, max(0, size - 1)
    while lo <= hi:
        mid = (lo + hi) // 2
        if mid == target:
            return  True
        if mid < target:
            lo = mid + 1
        else:
            hi = mid - 1
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
    print(f"found: {bsearch(size, target)}")


if __name__ == "__main__":
    main()

