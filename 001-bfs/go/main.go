package main

import (
    "fmt"
    "os"
    "strconv"
)

// Minimal, didactic BFS on an implicit complete binary tree.
// Nodes are labeled 0..size-1. For i: left=2*i+1, right=2*i+2 when < size.

func bfs(size, target int) bool {
    if size == 0 {
        return false
    }
    // Simple FIFO queue using a slice; append to push, re-slice to pop.
    q := make([]int, 0, 16)
    q = append(q, 0) // root index
    for len(q) > 0 {
        i := q[0]
        q = q[1:]
        if i == target {
            return true
        }
        l := 2*i + 1
        r := 2*i + 2
        if l < size {
            q = append(q, l)
        }
        if r < size {
            q = append(q, r)
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

    fmt.Printf("found: %v\n", bfs(size, target))
}

