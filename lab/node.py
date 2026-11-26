"""One throwaway bitcoind in regtest, and a JSON-RPC client for it.

The node gets a fresh datadir under a mktemp directory, does not listen for peers, makes no
outbound connections, answers RPC only on 127.0.0.1 at an unusual port above 28000, and is stopped
and its datadir deleted when the `with` block ends, whether the block succeeded or not. It never
reads or writes ~/.bitcoin and cannot run on any network but regtest.
"""

from __future__ import annotations

import base64
import json
import random
import shutil
import signal
import socket
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

RESERVED_PORTS = {18443, 18444, 18993, 28332, 28333}


class RPCError(Exception):
    def __init__(self, code: int, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def free_port() -> int:
    """A port in 28100..28999 that nothing on 127.0.0.1 is bound to right now."""
    for _ in range(200):
        port = random.randint(28100, 28999)
        if port in RESERVED_PORTS:
            continue
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
            except OSError:
                continue
        return port
    raise RuntimeError("no free port in 28100..28999")


class Node:
    def __init__(self, bitcoind: Path, keep: bool = False):
        self.bitcoind = Path(bitcoind)
        self.keep = keep
        self.tmp: Path | None = None
        self.proc: subprocess.Popen | None = None
        self.port = 0
        self._auth = ""
        self._id = 0

    # lifecycle ---------------------------------------------------------------------------------

    def __enter__(self) -> "Node":
        self._old_handlers = {}
        for sig in (signal.SIGTERM, signal.SIGHUP):
            self._old_handlers[sig] = signal.signal(sig, self._on_signal)
        try:
            self.start()
        except BaseException:
            self.stop()
            raise
        return self

    def __exit__(self, *exc) -> None:
        self.stop()
        for sig, handler in self._old_handlers.items():
            signal.signal(sig, handler)

    @staticmethod
    def _on_signal(signum, frame):
        raise SystemExit(128 + signum)

    def start(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="escapement-regtest-"))
        datadir = self.tmp / "data"
        datadir.mkdir()
        self.port = free_port()
        args = [
            str(self.bitcoind),
            "-regtest",
            f"-datadir={datadir}",
            "-listen=0",
            "-connect=0",
            "-dnsseed=0",
            "-fixedseeds=0",
            "-server=1",
            "-rpcbind=127.0.0.1",
            "-rpcallowip=127.0.0.1",
            f"-rpcport={self.port}",
            "-fallbackfee=0.0001",
            "-txindex=1",
            "-acceptnonstdtxn=0",
            "-printtoconsole=0",
        ]
        self.proc = subprocess.Popen(args, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                     stderr=subprocess.PIPE)
        cookie = datadir / "regtest" / ".cookie"
        deadline = time.monotonic() + 60
        while True:
            if self.proc.poll() is not None:
                err = self.proc.stderr.read().decode(errors="replace") if self.proc.stderr else ""
                raise RuntimeError(f"bitcoind exited with {self.proc.returncode}: {err.strip()}")
            if cookie.exists():
                self._auth = base64.b64encode(cookie.read_bytes().strip()).decode()
                try:
                    chain = self.rpc("getblockchaininfo")["chain"]
                    if chain != "regtest":
                        raise RuntimeError(f"node reports chain {chain!r}, refusing to continue")
                    return
                except RPCError as e:
                    if e.code != -28:  # -28: still warming up
                        raise
                except (ConnectionError, urllib.error.URLError, OSError):
                    pass
            if time.monotonic() > deadline:
                raise RuntimeError("bitcoind did not answer RPC within 60 s")
            time.sleep(0.1)

    def stop(self) -> None:
        if self.proc is not None and self.proc.poll() is None:
            try:
                self.rpc("stop")
            except Exception:
                pass
            try:
                self.proc.wait(timeout=60)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait(timeout=10)
        self.proc = None
        if self.tmp is not None and not self.keep:
            shutil.rmtree(self.tmp, ignore_errors=True)
            self.tmp = None

    # RPC -----------------------------------------------------------------------------------------

    def rpc(self, method: str, *params):
        self._id += 1
        body = json.dumps({"jsonrpc": "1.0", "id": self._id, "method": method,
                           "params": list(params)}).encode()
        req = urllib.request.Request(
            f"http://127.0.0.1:{self.port}/", data=body,
            headers={"Authorization": f"Basic {self._auth}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                reply = json.loads(resp.read())
        except urllib.error.HTTPError as e:
            payload = e.read()
            try:
                reply = json.loads(payload)
            except ValueError:
                raise RPCError(e.code, payload.decode(errors="replace")) from None
        if reply.get("error"):
            raise RPCError(reply["error"]["code"], reply["error"]["message"])
        return reply["result"]
