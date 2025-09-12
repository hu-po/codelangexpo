use std::env;

// Minimal, didactic binary search on an implicit sorted array
// where arr[i] = i for 0 <= i < size.

fn bsearch(size: usize, target: usize) -> bool {
    if size == 0 { return false; }
    let mut lo: isize = 0;
    let mut hi: isize = (size as isize) - 1;
    let t: isize = target as isize;
    while lo <= hi {
        let mid = lo + (hi - lo) / 2;
        if mid == t { return true; }
        if mid < t { lo = mid + 1; } else { hi = mid - 1; }
    }
    false
}

fn main() {
    // Args: <size> <target>, defaults: 100000, size-1
    let args: Vec<String> = env::args().collect();
    let size: usize = args.get(1).and_then(|s| s.parse().ok()).unwrap_or(100_000);
    let target: usize = args.get(2).and_then(|s| s.parse().ok()).unwrap_or_else(|| size.saturating_sub(1));

    println!("found: {}", bsearch(size, target));
}

