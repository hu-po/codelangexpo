#include <bits/stdc++.h>
using namespace std;

// Minimal, didactic binary search on an implicit sorted array.
// The array is conceptual: arr[i] = i for 0 <= i < size.

static bool bsearch_ll(long long size, long long target) {
    if (size <= 0) return false;
    long long lo = 0, hi = size - 1;
    while (lo <= hi) {
        long long mid = lo + (hi - lo) / 2;
        if (mid == target) return true;
        if (mid < target) lo = mid + 1; else hi = mid - 1;
    }
    return false;
}

int main(int argc, char** argv) {
    long long size = 100000;
    long long target = size - 1;
    if (argc > 1) size = max(0LL, atoll(argv[1]));
    if (argc > 2) target = max(0LL, atoll(argv[2]));
    cout << boolalpha << "found: " << bsearch_ll(size, target) << "\n";
}

