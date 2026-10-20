"""Experiment 8: request-response file server over TCP (port 6000).

    python3 tcp_file_server.py [--lan] [--slow]

Same wire protocol as the manual (filename line -> "OK <size> <sha256>" ->
raw bytes), but built on socketserver.ThreadingTCPServer so several clients can
be served at the same time and one broken transfer cannot kill the server.
"""
import argparse
import hashlib
import socketserver
import time
from pathlib import Path

PORT = 6000
FILES_FOLDER = Path("server_files")
CHUNK_SIZE = 1024
SLOW_DEMO = False                 # set by --slow: pause after each chunk


def safe_path(name: str) -> Path | None:
    """Return the real path inside FILES_FOLDER, or None if the name is unsafe."""
    if not name or name != Path(name).name or ".." in name:
        return None
    candidate = (FILES_FOLDER / name).resolve()
    root = FILES_FOLDER.resolve()
    if root not in candidate.parents:          # never escape the shared folder
        return None
    return candidate if candidate.is_file() else None


def digest(path: Path) -> str:
    sha = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            sha.update(block)
    return sha.hexdigest()


class FileHandler(socketserver.StreamRequestHandler):
    timeout = 15

    def handle(self) -> None:
        peer = f"{self.client_address[0]}:{self.client_address[1]}"
        try:
            requested = self.rfile.readline(256).decode().strip()
        except (OSError, UnicodeDecodeError) as error:
            print(f"[server] {peer} bad request: {error}")
            return
        if not requested:
            print(f"[server] {peer} closed without sending a request")
            return
        print(f"[server] {peer} asked for {requested!r}")

        if not requested or requested != Path(requested).name or ".." in requested:
            self.wfile.write(b"ERROR Invalid filename\n")
            print(f"[server] {peer} rejected: invalid filename")
            return

        path = safe_path(requested)
        if path is None:
            self.wfile.write(b"ERROR File not found\n")
            print(f"[server] {peer} rejected: file not found")
            return

        size = path.stat().st_size
        self.wfile.write(f"OK {size} {digest(path)}\n".encode())

        start = time.perf_counter()
        sent = 0
        try:
            with path.open("rb") as handle:
                while chunk := handle.read(CHUNK_SIZE):
                    self.wfile.write(chunk)
                    sent += len(chunk)
                    if SLOW_DEMO:
                        time.sleep(0.05)
            self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError, OSError) as error:
            print(f"[server] {peer} transfer aborted after {sent} bytes: {error}")
            return
        elapsed = time.perf_counter() - start
        rate = (sent / 1024) / elapsed if elapsed else 0
        print(f"[server] {peer} sent {sent} bytes in {elapsed:.4f} s ({rate:.0f} KB/s)")


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--lan", action="store_true", help="listen on every interface")
    ap.add_argument("--slow", action="store_true", help="pause 50 ms per chunk")
    args = ap.parse_args()
    SLOW_DEMO = args.slow
    host = "0.0.0.0" if args.lan else "127.0.0.1"

    with Server((host, PORT), FileHandler) as server:
        print(f"[server] TCP file server on {host}:{PORT}, sharing {FILES_FOLDER}/")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n[server] stopped by Ctrl+C")
