#include <bits/stdc++.h>
using namespace std;

// Minimal, didactic BFS on an implicit complete binary tree.
// Nodes are 0..size-1; children: left=2*i+1, right=2*i+2 if < size.

static bool bfs(size_t size, size_t target) {
    if (size == 0) return false;
    deque<size_t> q;         // FIFO queue of node indices
    q.push_back(0);          // start from root
    while (!q.empty()) {
        size_t i = q.front(); q.pop_front();
        if (i == target) return true; // found
        size_t l = 2*i + 1;
        size_t r = 2*i + 2;
        if (l < size) q.push_back(l);
        if (r < size) q.push_back(r);
    }
    return false;
}

int main(int argc, char** argv) {
    size_t size = 100000;
    size_t target = size - 1;
    if (argc > 1) size = max(0LL, atoll(argv[1]));
    if (argc > 2) target = max(0LL, atoll(argv[2]));
    cout << boolalpha << "found: " << bfs(size, target) << "\n";
}

