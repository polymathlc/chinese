#!/usr/bin/env python3
"""Apply a proven UTF-8 delta manifest and stage only its intended paths.

Run at the repository root. The checked-out helper commit must contain the exact
remote baseline sources used to construct the manifest, including their original
leading/trailing newlines. No source file is modified before every hash validates.
"""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

HELPERS = (
    ".github/workflows/codex-publish-model-defaults.yml",
    ".codex-publish/apply-model-deltas.py",
    ".codex-publish/model-deltas.json",
)

def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()

def blob_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()

def checked_path(value):
    if not isinstance(value, str) or not value or "\0" in value or "\\" in value:
        raise ValueError("Invalid manifest path")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in (".", "..", ".git") for part in path.parts):
        raise ValueError("Unsafe manifest path: " + value)
    if str(path) != value or value in HELPERS:
        raise ValueError("Non-canonical or reserved manifest path: " + value)
    for part in [Path(value), *Path(value).parents]:
        if part.is_symlink():
            raise ValueError("Symlinks are not supported: " + value)
    return Path(value)

def require_sha(value, label):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{40}", value):
        raise ValueError("Invalid SHA for " + label)
    return value

def main():
    manifest_path = sys.argv[1] if len(sys.argv) > 1 else HELPERS[2]
    root = Path(git("rev-parse", "--show-toplevel")).resolve()
    if Path.cwd().resolve() != root:
        raise ValueError("Run the builder at the repository root")
    expected_head = os.environ.get("GITHUB_SHA")
    if expected_head and git("rev-parse", "HEAD") != expected_head:
        raise ValueError("Checkout HEAD differs from the triggering commit")
    if git("status", "--porcelain"):
        raise ValueError("The checkout must be clean before applying deltas")
    manifest = json.loads(Path(manifest_path).read_bytes().decode("utf-8"))
    if not isinstance(manifest, list) or not manifest:
        raise ValueError("Expected a non-empty list of file deltas")
    plans = []
    seen = set()
    for delta in manifest:
        path = checked_path(delta["path"])
        if str(path) in seen:
            raise ValueError("Duplicate manifest path: " + str(path))
        seen.add(str(path))
        expected = require_sha(delta["expectedSha"], str(path))
        has_ops, has_content = "ops" in delta, "content" in delta
        if has_ops == has_content:
            raise ValueError("Each delta requires exactly one of ops or content")
        if has_ops:
            baseline = path.read_bytes()
            if blob_sha(baseline) != require_sha(delta["baseSha"], str(path)):
                raise ValueError("Baseline blob SHA differs: " + str(path))
            lines = baseline.decode("utf-8").splitlines(keepends=True)
            ops = delta["ops"]
            if not isinstance(ops, list):
                raise ValueError("Invalid ops list: " + str(path))
            previous_end = -1
            for op in ops:
                start, delete, insert = op["start"], op["delete"], op["insert"]
                if type(start) is not int or type(delete) is not int or not isinstance(insert, str):
                    raise ValueError("Invalid delta operation: " + str(path))
                if start < 0 or delete < 0 or start + delete > len(lines) or start < previous_end:
                    raise ValueError("Overlapping or out-of-bounds delta: " + str(path))
                previous_end = start + delete
            for op in reversed(ops):
                lines[op["start"]:op["start"] + op["delete"]] = [op["insert"]]
            result = "".join(lines).encode("utf-8")
        else:
            if not isinstance(delta["content"], str):
                raise ValueError("New file content must be UTF-8 text")
            result = delta["content"].encode("utf-8")
            if path.exists() and path.read_bytes() != result:
                raise ValueError("New file already exists with different content: " + str(path))
        if blob_sha(result) != expected:
            raise ValueError("Final blob SHA differs: " + str(path))
        if type(delta.get("bytes")) is not int or len(result) != delta["bytes"]:
            raise ValueError("Final byte count differs: " + str(path))
        plans.append((path, result, expected))
    # All baselines and final outputs are proven before any write.
    for path, result, expected in plans:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(result)
        if blob_sha(path.read_bytes()) != expected:
            raise ValueError("Written blob SHA differs: " + str(path))
    subprocess.run(["git", "add", "--", *sorted(seen)], check=True)
    staged = set(subprocess.check_output(["git", "diff", "--cached", "--name-only", "-z"]).decode().rstrip("\0").split("\0"))
    staged.discard("")
    if not staged or not staged.issubset(seen):
        raise ValueError("Staged changes must be non-empty and contain only manifest paths")
    if any(path.startswith(".github/workflows/") for path in staged):
        raise ValueError("Pre-create workflow changes through the connector; the Actions token must not change workflows")
    subprocess.run(["git", "diff", "--cached", "--check"], check=True)
    for path, _, expected in plans:
        if git("rev-parse", ":" + str(path)) != expected:
            raise ValueError("Staged blob SHA differs: " + str(path))
    print("Validated", len(plans), "exact model-default files; staged", len(staged), "changed files. Helpers require connector cleanup.")

if __name__ == "__main__":
    main()
