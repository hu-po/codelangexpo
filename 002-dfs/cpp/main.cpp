#include <bits/stdc++.h>
using namespace std;

// Minimal, didactic iterative DFS (explicit stack) on an implicit tree.
// Nodes: 0..size-1; children: 2*i+1 and 2*i+2 if < size.

static bool dfs(size_t size, size_t target) {
    if (size == 0) return false;
    vector<size_t> st; st.push_back(0); // seed with root
    while (!st.empty()) {
        size_t i = st.back(); st.pop_back();
        if (i == target) return true;
        size_t l = 2*i + 1;
        size_t r = 2*i + 2;
        if (r < size) st.push_back(r); // push right first
        if (l < size) st.push_back(l); // then left (processed first)
    }
    return false;
}

int main(int argc, char** argv) {
    size_t size = 100000;
    size_t target = size - 1;
    if (argc > 1) size = max(0LL, atoll(argv[1]));
    if (argc > 2) target = max(0LL, atoll(argv[2]));
    cout << boolalpha << "found: " << dfs(size, target) << "\n";
}

