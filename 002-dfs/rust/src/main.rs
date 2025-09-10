use std::env;

// Minimal, didactic iterative DFS (using an explicit stack) over an
// implicit complete binary tree (0..size-1). For i: left=2*i+1, right=2*i+2.

fn dfs(size: usize, target: usize) -> bool {
    if size == 0 { return false; }
    let mut st: Vec<usize> = vec![0]; // stack seeded with root
    while let Some(i) = st.pop() {
        if i == target { return true; }
        // Push right first, then left: this ensures left is processed first
        // (LIFO stack pops the last pushed element).
        let l = 2*i + 1;
        let r = 2*i + 2;
        if r < size { st.push(r); }
        if l < size { st.push(l); }
    }
    false
}

fn main() {
    // Args: <size> <target>, defaults: 100000, size-1
    let args: Vec<String> = env::args().collect();
    let size: usize = args.get(1).and_then(|s| s.parse().ok()).unwrap_or(100_000);
    let target: usize = args.get(2).and_then(|s| s.parse().ok()).unwrap_or_else(|| size.saturating_sub(1));

    let found = dfs(size, target);
    println!("found: {}", found);
}

