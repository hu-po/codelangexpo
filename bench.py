#!/usr/bin/env python3
import argparse
import os
import shutil
import subprocess
import sys
import time
import re


def exe(name: str) -> str:
    return name + (".exe" if os.name == "nt" else "")


def run(cmd, cwd=None):
    return subprocess.run(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def time_run(cmd, cwd=None):
    t0 = time.perf_counter()
    proc = run(cmd, cwd=cwd)
    t1 = time.perf_counter()
    return proc, (t1 - t0)


def build_rust(path):
    if shutil.which("cargo") is None:
        return False, "cargo not found", None, None
    proc, dur = time_run(["cargo", "build", "--release"], cwd=path)
    if proc.returncode != 0:
        return False, proc.stderr.strip(), dur, None
    return True, "ok", dur, None


def cargo_pkg_name(path):
    toml = os.path.join(path, "Cargo.toml")
    try:
        with open(toml, "r", encoding="utf-8") as f:
            in_pkg = False
            for line in f:
                s = line.strip()
                if s.startswith("[") and s.endswith("]"):
                    in_pkg = (s == "[package]")
                elif in_pkg:
                    m = re.match(r'^name\s*=\s*"([^"]+)"', s)
                    if m:
                        return m.group(1)
    except FileNotFoundError:
        return None
    return None


def build_go(path):
    if shutil.which("go") is None:
        return False, "go not found", None, None
    out_name = exe("app")
    proc, dur = time_run(["go", "build", "-o", out_name], cwd=path)
    if proc.returncode != 0:
        return False, proc.stderr.strip(), dur, None
    return True, "ok", dur, os.path.join(path, out_name)


def build_cpp(path):
    if shutil.which("g++") is None:
        return False, "g++ not found", None, None
    out_name = exe("app")
    proc, dur = time_run(["g++", "-O2", "-std=c++17", "-o", out_name, "main.cpp"], cwd=path)
    if proc.returncode != 0:
        return False, proc.stderr.strip(), dur, None
    return True, "ok", dur, os.path.join(path, out_name)


def run_all(problem, size, target, build=True):
    results = []

    # Rust
    rust_dir = os.path.join(problem, "rust")
    if build:
        ok, msg, btime, _ = build_rust(rust_dir)
        results.append({"lang": "rust-build", "ok": ok, "message": msg, "time": btime})
    # Prefer running the compiled binary directly for fair timing
    pkg = cargo_pkg_name(rust_dir)
    if pkg:
        rust_bin_rel = os.path.join("target", "release", exe(pkg))
        rust_bin = os.path.join(rust_dir, rust_bin_rel)
        if os.path.exists(rust_bin):
            proc, rtime = time_run(["./" + os.path.join("target", "release", exe(pkg)), str(size), str(target)], cwd=rust_dir)
            results.append({"lang": "rust", "ok": proc.returncode == 0, "message": (proc.stdout or proc.stderr).strip(), "time": rtime})
        else:
            # Fallback to cargo run if binary missing
            if shutil.which("cargo") is not None and os.path.isdir(rust_dir):
                proc, rtime = time_run(["cargo", "run", "--quiet", "--release", "--", str(size), str(target)], cwd=rust_dir)
                results.append({"lang": "rust", "ok": proc.returncode == 0, "message": (proc.stdout or proc.stderr).strip(), "time": rtime})
            else:
                results.append({"lang": "rust", "ok": False, "message": "binary not found", "time": None})
    else:
        results.append({"lang": "rust", "ok": False, "message": "Cargo.toml name not found", "time": None})

    # Go
    go_dir = os.path.join(problem, "go")
    go_bin_name = exe("app")
    go_bin = os.path.join(go_dir, go_bin_name)
    if build:
        ok, msg, btime, built_bin = build_go(go_dir)
        results.append({"lang": "go-build", "ok": ok, "message": msg, "time": btime})
        if ok and built_bin:
            go_bin = built_bin
    if os.path.exists(go_bin):
        proc, rtime = time_run(["./" + go_bin_name, str(size), str(target)], cwd=go_dir)
        results.append({"lang": "go", "ok": proc.returncode == 0, "message": (proc.stdout or proc.stderr).strip(), "time": rtime})
    else:
        # Fallback to `go run .` if binary absent
        if shutil.which("go") is not None and os.path.isdir(go_dir):
            proc, rtime = time_run(["go", "run", ".", str(size), str(target)], cwd=go_dir)
            results.append({"lang": "go", "ok": proc.returncode == 0, "message": (proc.stdout or proc.stderr).strip(), "time": rtime})
        else:
            results.append({"lang": "go", "ok": False, "message": "binary not found", "time": None})

    # C++
    cpp_dir = os.path.join(problem, "cpp")
    cpp_bin_name = exe("app")
    cpp_bin = os.path.join(cpp_dir, cpp_bin_name)
    if build:
        ok, msg, btime, built_bin = build_cpp(cpp_dir)
        results.append({"lang": "cpp-build", "ok": ok, "message": msg, "time": btime})
        if ok and built_bin:
            cpp_bin = built_bin
    if os.path.exists(cpp_bin):
        proc, rtime = time_run(["./" + cpp_bin_name, str(size), str(target)], cwd=cpp_dir)
        results.append({"lang": "cpp", "ok": proc.returncode == 0, "message": (proc.stdout or proc.stderr).strip(), "time": rtime})
    else:
        results.append({"lang": "cpp", "ok": False, "message": "binary not found", "time": None})

    # Python
    py_dir = os.path.join(problem, "python")
    py_main_name = "main.py"
    py_main = os.path.join(py_dir, py_main_name)
    py_exec = sys.executable or "python3"
    if os.path.exists(py_main):
        proc, rtime = time_run([py_exec, py_main_name, str(size), str(target)], cwd=py_dir)
        results.append({"lang": "python", "ok": proc.returncode == 0, "message": (proc.stdout or proc.stderr).strip(), "time": rtime})
    else:
        results.append({"lang": "python", "ok": False, "message": "main.py not found", "time": None})

    return results


def main():
    ap = argparse.ArgumentParser(description="Benchmark harness to compare implementations across languages")
    ap.add_argument("--problem", default="001-bfs", help="problem directory (e.g., 001-bfs or 002-dfs)")
    ap.add_argument("--size", type=int, default=100_000, help="number of nodes")
    ap.add_argument("--target", type=int, default=-1, help="value to find (default size-1)")
    ap.add_argument("--no-build", action="store_true", help="skip build steps and run existing binaries")
    args = ap.parse_args()

    target = args.target if args.target >= 0 else (args.size - 1 if args.size > 0 else 0)

    results = run_all(args.problem, args.size, target, build=(not args.no_build))

    print("\n=== Benchmark Summary ===")
    for r in results:
        lang = r["lang"]
        ok = "ok" if r["ok"] else "FAIL"
        t = (f"{r['time']:.4f}s" if isinstance(r["time"], float) else "-")
        msg = r["message"]
        if len(msg) > 120:
            msg = msg[:117] + "..."
        print(f"{lang:10} | {ok:4} | {t:>8} | {msg}")


if __name__ == "__main__":
    main()
