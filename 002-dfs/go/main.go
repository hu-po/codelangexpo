package main

import (
    "fmt"
    "os"
    "strconv"
)

// Minimal, didactic iterative DFS using an explicit stack.
// Implicit complete binary tree: nodes 0..size-1; children 2*i+1 and 2*i+2 if < size.

func dfs(size, target int) bool {
    if size == 0 {
        return false
    }
    st := make([]int, 0, 16)
    st = append(st, 0) // root
    for len(st) > 0 {
        i := st[len(st)-1]
        st = st[:len(st)-1]
        if i == target {
            return true
        }
        l := 2*i + 1
        r := 2*i + 2
        // Push right first so left is processed first when popped
        if r < size {
            st = append(st, r)
        }
        if l < size {
            st = append(st, l)
        }
    }
    return false
}

func main() {
    // Args: <size> <target>, defaults: 100000, size-1
    size := 100000
    target := size - 1
    if len(os.Args) > 1 {
        if v, err := strconv.Atoi(os.Args[1]); err == nil {
            size = v
            target = size - 1
        }
    }
    if len(os.Args) > 2 {
        if v, err := strconv.Atoi(os.Args[2]); err == nil {
            target = v
        }
    }
    fmt.Printf("found: %v\n", dfs(size, target))
}

