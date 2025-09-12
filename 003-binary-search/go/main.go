package main

import (
    "fmt"
    "os"
    "strconv"
)

// Minimal, didactic binary search on an implicit sorted array
// where arr[i] == i for 0 <= i < size.

func bsearch(size, target int) bool {
    if size <= 0 {
        return false
    }
    lo, hi := 0, size-1
    for lo <= hi {
        mid := lo + (hi-lo)/2
        if mid == target {
            return true
        }
        if mid < target {
            lo = mid + 1
        } else {
            hi = mid - 1
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
            if v < 0 {
                v = 0
            }
            size = v
            target = size - 1
        }
    }
    if len(os.Args) > 2 {
        if v, err := strconv.Atoi(os.Args[2]); err == nil {
            if v < 0 {
                v = 0
            }
            target = v
        }
    }
    fmt.Printf("found: %v\n", bsearch(size, target))
}

