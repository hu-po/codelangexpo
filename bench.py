#!/usr/bin/env python3
import argparse
import os
import shutil
import subprocess
import sys
import time
import re
from typing import List, Optional


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


def summarize_times(times: List[float]):
    if not times:
        return None, ""
    avg = sum(times) / len(times)
    mn = min(times)
    mx = max(times)
    return avg, f"n={len(times)} min={mn:.4f}s max={mx:.4f}s"


def run_all(problem, size, target, build=True, runs: int = 1):
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
            times: List[float] = []
            ok_all = True
            last_msg = ""
            for _ in range(max(1, runs)):
                proc, rtime = time_run(["./" + os.path.join("target", "release", exe(pkg)), str(size), str(target)], cwd=rust_dir)
                times.append(rtime)
                ok_all = ok_all and (proc.returncode == 0)
                last_msg = (proc.stdout or proc.stderr).strip()
            avg, extra = summarize_times(times)
            results.append({"lang": "rust", "ok": ok_all, "message": f"{last_msg} ({extra})".strip(), "time": avg, "times": times})
        else:
            # Fallback to cargo run if binary missing
            if shutil.which("cargo") is not None and os.path.isdir(rust_dir):
                times: List[float] = []
                ok_all = True
                last_msg = ""
                for _ in range(max(1, runs)):
                    proc, rtime = time_run(["cargo", "run", "--quiet", "--release", "--", str(size), str(target)], cwd=rust_dir)
                    times.append(rtime)
                    ok_all = ok_all and (proc.returncode == 0)
                    last_msg = (proc.stdout or proc.stderr).strip()
                avg, extra = summarize_times(times)
                results.append({"lang": "rust", "ok": ok_all, "message": f"{last_msg} ({extra})".strip(), "time": avg, "times": times})
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
        times: List[float] = []
        ok_all = True
        last_msg = ""
        for _ in range(max(1, runs)):
            proc, rtime = time_run(["./" + go_bin_name, str(size), str(target)], cwd=go_dir)
            times.append(rtime)
            ok_all = ok_all and (proc.returncode == 0)
            last_msg = (proc.stdout or proc.stderr).strip()
        avg, extra = summarize_times(times)
        results.append({"lang": "go", "ok": ok_all, "message": f"{last_msg} ({extra})".strip(), "time": avg, "times": times})
    else:
        # Fallback to `go run .` if binary absent
        if shutil.which("go") is not None and os.path.isdir(go_dir):
            times: List[float] = []
            ok_all = True
            last_msg = ""
            for _ in range(max(1, runs)):
                proc, rtime = time_run(["go", "run", ".", str(size), str(target)], cwd=go_dir)
                times.append(rtime)
                ok_all = ok_all and (proc.returncode == 0)
                last_msg = (proc.stdout or proc.stderr).strip()
            avg, extra = summarize_times(times)
            results.append({"lang": "go", "ok": ok_all, "message": f"{last_msg} ({extra})".strip(), "time": avg, "times": times})
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
        times: List[float] = []
        ok_all = True
        last_msg = ""
        for _ in range(max(1, runs)):
            proc, rtime = time_run(["./" + cpp_bin_name, str(size), str(target)], cwd=cpp_dir)
            times.append(rtime)
            ok_all = ok_all and (proc.returncode == 0)
            last_msg = (proc.stdout or proc.stderr).strip()
        avg, extra = summarize_times(times)
        results.append({"lang": "cpp", "ok": ok_all, "message": f"{last_msg} ({extra})".strip(), "time": avg, "times": times})
    else:
        results.append({"lang": "cpp", "ok": False, "message": "binary not found", "time": None})

    # Python
    py_dir = os.path.join(problem, "python")
    py_main_name = "main.py"
    py_main = os.path.join(py_dir, py_main_name)
    py_exec = sys.executable or "python3"
    if os.path.exists(py_main):
        times: List[float] = []
        ok_all = True
        last_msg = ""
        for _ in range(max(1, runs)):
            proc, rtime = time_run([py_exec, py_main_name, str(size), str(target)], cwd=py_dir)
            times.append(rtime)
            ok_all = ok_all and (proc.returncode == 0)
            last_msg = (proc.stdout or proc.stderr).strip()
        avg, extra = summarize_times(times)
        results.append({"lang": "python", "ok": ok_all, "message": f"{last_msg} ({extra})".strip(), "time": avg, "times": times})
    else:
        results.append({"lang": "python", "ok": False, "message": "main.py not found", "time": None})

    return results


def main():
    ap = argparse.ArgumentParser(description="Benchmark harness to compare implementations across languages")
    ap.add_argument("--problem", default="001-bfs", help="problem directory (e.g., 001-bfs or 002-dfs)")
    ap.add_argument("--size", type=int, default=100_000, help="number of nodes")
    ap.add_argument("--target", type=int, default=-1, help="value to find (default size-1)")
    ap.add_argument("--no-build", action="store_true", help="skip build steps and run existing binaries")
    ap.add_argument("--runs", type=int, default=1, help="number of times to run each language implementation")
    ap.add_argument("--plot", default="bench.png", help="output PNG file path for scatter plot of per-run times")
    args = ap.parse_args()

    target = args.target if args.target >= 0 else (args.size - 1 if args.size > 0 else 0)

    results = run_all(args.problem, args.size, target, build=(not args.no_build), runs=max(1, args.runs))

    print("\n=== Benchmark Summary ===")
    for r in results:
        lang = r["lang"]
        ok = "ok" if r["ok"] else "FAIL"
        t = (f"{r['time']:.4f}s" if isinstance(r["time"], float) else "-")
        msg = r["message"]
        if len(msg) > 120:
            msg = msg[:117] + "..."
        print(f"{lang:10} | {ok:4} | {t:>8} | {msg}")

    # Save scatter plot of per-run times if possible
    def save_scatter(results, path, title):
        try:
            import matplotlib
            matplotlib.use("Agg")  # non-interactive backend
            import matplotlib.pyplot as plt
        except Exception as e:
            print(f"plot: unable to import matplotlib: {e}")
            return False

        langs = []
        series = []
        for r in results:
            if r.get("lang") in ("rust", "go", "cpp", "python") and r.get("times"):
                langs.append(r["lang"])
                series.append(r["times"])

        if not series:
            print("plot: no per-run timing data available")
            return False

        plt.figure(figsize=(8, 4.5))
        for idx, (lang, times) in enumerate(zip(langs, series)):
            xs = list(range(1, len(times) + 1))
            plt.scatter(xs, times, label=lang, s=18)

        plt.xlabel("run")
        plt.ylabel("time (s)")
        plt.title(title)
        plt.legend()
        plt.grid(True, alpha=0.25)
        try:
            plt.tight_layout()
            plt.savefig(path, dpi=150)
            print(f"plot: saved scatter to {path}")
            return True
        except Exception as e:
            print(f"plot: failed to save {path}: {e}")
            return False

    title = f"{args.problem} size={args.size} target={target} runs={max(1, args.runs)}"
    save_scatter(results, args.plot, title)


if __name__ == "__main__":
    main()
