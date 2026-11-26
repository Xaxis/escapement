#!/usr/bin/env python3
"""Fetch the pinned Bitcoin Core release and test framework files, idempotently.

Reads lab/bitcoin-core.txt. Everything lands under ~/.cache/escapement/ (or $ESCAPEMENT_CACHE),
never in the repository:

  bitcoin-<version>/bin/bitcoind          the release binary, unpacked from the verified tarball
  downloads/<version>/                    the tarball and the release's SHA256SUMS
  test_framework/<tag>/test_framework/    Bitcoin Core's functional test framework files (MIT)

The tarball must match both the hash pinned in bitcoin-core.txt and its line in the release's
SHA256SUMS. Each framework file must match its pinned sha256. A run with everything in place and
verified makes no network request. This script does not check the release's GPG signatures; the
README says how to.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
PINS = HERE / "bitcoin-core.txt"
CACHE = Path(os.environ.get("ESCAPEMENT_CACHE", Path.home() / ".cache" / "escapement"))
AGENT = "escapement-lab-fetch/1"


def pins() -> dict:
    out: dict = {"file": {}}
    for line in PINS.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, rest = line.partition(" ")
        if key == "file":
            name, sha = rest.split()
            out["file"][name] = sha
        else:
            out[key] = rest.strip()
    return out


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + ".part")
    req = urllib.request.Request(url, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(req, timeout=120) as resp, tmp.open("wb") as out:
        shutil.copyfileobj(resp, out)
    tmp.replace(dest)


def framework_root(p: dict | None = None) -> Path:
    """The directory to put on sys.path so that `import test_framework` finds the pinned files."""
    p = p or pins()
    return CACHE / "test_framework" / p["tag"]


def ensure_bitcoind(p: dict) -> Path:
    version, tarball, want = p["version"], p["tarball"], p["tarball_sha256"]
    root = CACHE / f"bitcoin-{version}"
    marker = root / ".escapement-verified"
    binary = root / "bin" / "bitcoind"
    if binary.exists() and marker.exists() and marker.read_text().strip() == want:
        return binary
    dl = CACHE / "downloads" / version
    sums = dl / "SHA256SUMS"
    tar = dl / tarball
    download(p["release_url"] + "SHA256SUMS", sums)
    listed = {}
    for line in sums.read_text().splitlines():
        parts = line.split()
        if len(parts) == 2:
            listed[parts[1].lstrip("*")] = parts[0]
    if listed.get(tarball) != want:
        sys.exit(f"fetch: SHA256SUMS lists {listed.get(tarball)!r} for {tarball}, pinned {want}")
    if not tar.exists() or sha256_file(tar) != want:
        print(f"fetch: downloading {tarball}", file=sys.stderr)
        download(p["release_url"] + tarball, tar)
    got = sha256_file(tar)
    if got != want:
        tar.unlink()
        sys.exit(f"fetch: {tarball} has sha256 {got}, pinned {want}")
    stage = Path(tempfile.mkdtemp(prefix="unpack-", dir=CACHE))
    try:
        with tarfile.open(tar) as tf:
            tf.extractall(stage, filter="data")
        unpacked = stage / f"bitcoin-{version}"
        if not (unpacked / "bin" / "bitcoind").exists():
            sys.exit(f"fetch: {tarball} has no bitcoin-{version}/bin/bitcoind")
        if root.exists():
            shutil.rmtree(root)
        unpacked.rename(root)
    finally:
        shutil.rmtree(stage, ignore_errors=True)
    marker.write_text(want + "\n")
    print(f"fetch: bitcoind {version} verified ({want}) at {binary}", file=sys.stderr)
    return binary


def ensure_framework(p: dict) -> Path:
    root = framework_root(p)
    pkg = root / "test_framework"
    for name, want in p["file"].items():
        dest = pkg / name
        if dest.exists() and sha256_file(dest) == want:
            continue
        print(f"fetch: test_framework/{name} at {p['tag']}", file=sys.stderr)
        download(p["source_url"] + name, dest)
        got = sha256_file(dest)
        if got != want:
            dest.unlink()
            sys.exit(f"fetch: test_framework/{name} has sha256 {got}, pinned {want}")
    return root


def ensure() -> tuple[Path, Path]:
    """Make sure the binary and framework files are present and verified; return their paths."""
    p = pins()
    CACHE.mkdir(parents=True, exist_ok=True)
    return ensure_bitcoind(p), ensure_framework(p)


if __name__ == "__main__":
    binary, framework = ensure()
    print(f"bitcoind   {binary}")
    print(f"framework  {framework / 'test_framework'}")
