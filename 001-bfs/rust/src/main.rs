use std::collections::VecDeque;
use std::env;

// Minimal, didactic BFS over an implicit complete binary tree.
// - Nodes are 0..size-1
// - For node i, left=2*i+1, right=2*i+2 when < size

fn bfs(size: usize, target: usize) -> bool {
    if size == 0 { return false; }

    // Queue holds indices into the implicit tree
    let mut q: VecDeque<usize> = VecDeque::new();
    q.push_back(0); // start at root (index 0)

    while let Some(i) = q.pop_front() {
        if i == target { return true; } // found!

        // Compute children indices if they exist
        let l = 2*i + 1;
        let r = 2*i + 2;
        if l < size { q.push_back(l); }
        if r < size { q.push_back(r); }
    }
    false
}

fn main() {
    // Args: <size> <target>, defaults: 100000, size-1
    let args: Vec<String> = env::args().collect();
    let size: usize = args.get(1).and_then(|s| s.parse().ok()).unwrap_or(100_000);
    let target: usize = args.get(2).and_then(|s| s.parse().ok()).unwrap_or_else(|| size.saturating_sub(1));

    let found = bfs(size, target);
    println!("found: {}", found);
}

