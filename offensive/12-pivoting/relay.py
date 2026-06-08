#!/usr/bin/env python3
"""
TCP relay — simulates the pivot host's port-forwarding capability.

Usage: python3 relay.py LISTEN_ADDR LISTEN_PORT TARGET_HOST TARGET_PORT

This is the attacker's tunnel running on the compromised DMZ host.
It forwards connections from the attacker-accessible DMZ interface to the
internal target that only the pivot host can reach.

Real-world equivalents:
  chisel:    ./chisel server --reverse     (on attacker)
             ./chisel client <atk>:9001 R:8888:internal-target:80  (on pivot)
  ligolo-ng: agent on pivot; proxy on attacker adds route; fully transparent
  socat:     socat TCP-LISTEN:8888,fork TCP:internal-target:80
  SSH:       ssh -L 8888:internal-target:80 user@pivot
"""
import socket
import sys
import threading


def _pipe(src: socket.socket, dst: socket.socket) -> None:
    try:
        while chunk := src.recv(8192):
            dst.sendall(chunk)
    except OSError:
        pass
    finally:
        for s in (src, dst):
            try:
                s.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            try:
                s.close()
            except OSError:
                pass


def _handle(client: socket.socket, target_host: str, target_port: int) -> None:
    try:
        remote = socket.create_connection((target_host, target_port), timeout=5)
    except OSError as e:
        print(f"[relay] Cannot reach {target_host}:{target_port}: {e}", flush=True)
        client.close()
        return
    threading.Thread(target=_pipe, args=(client, remote), daemon=True).start()
    _pipe(remote, client)


def main() -> None:
    if len(sys.argv) != 5:
        print("Usage: relay.py LISTEN_ADDR LISTEN_PORT TARGET_HOST TARGET_PORT")
        sys.exit(1)

    listen_addr, listen_port, target_host, target_port = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((listen_addr, listen_port))
        srv.listen(20)
        print(f"[relay] {listen_addr}:{listen_port} → {target_host}:{target_port}", flush=True)
        while True:
            client, addr = srv.accept()
            threading.Thread(target=_handle, args=(client, target_host, target_port), daemon=True).start()


if __name__ == "__main__":
    main()
