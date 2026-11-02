#!/usr/bin/env python3
"""Query WHOIS servers over TCP and summarize the response."""
import argparse
import re
import socket

IANA = "whois.iana.org"

def query(server: str, term: str, port: int = 43, timeout: float = 10.0) -> str:
    with socket.create_connection((server, port), timeout=timeout) as sock:
        sock.sendall((term + "\r\n").encode())
        chunks = []
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            chunks.append(chunk)
    return b"".join(chunks).decode("utf-8", "replace")

def referral(text: str):
    match = re.search(r"^refer:\s*(\S+)", text, re.MULTILINE | re.IGNORECASE)
    return match.group(1) if match else None

def summarize(text: str):
    """Pull out the fields people usually want from a WHOIS record."""
    wanted = ["domain name", "registrar", "creation date", "updated date",
              "registry expiry date", "expiry date", "name server", "status"]
    found = {}
    for line in text.splitlines():
        key, _, value = line.partition(":")
        key = key.strip().lower()
        if key in wanted and value.strip():
            found.setdefault(key, []).append(value.strip())
    return found

SAMPLE = """Domain Name: EXAMPLE.COM
Registrar: RESERVED-Internet Assigned Numbers Authority
Creation Date: 1995-08-14T04:00:00Z
Updated Date: 2024-08-14T07:01:38Z
Registry Expiry Date: 2025-08-13T04:00:00Z
Name Server: A.IANA-SERVERS.NET
Name Server: B.IANA-SERVERS.NET
"""

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("term", nargs="?", help="domain or IP to look up")
    parser.add_argument("--server", default=IANA)
    parser.add_argument("--raw", action="store_true")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        for key, values in summarize(SAMPLE).items():
            for value in values:
                print(f"{key:<22} {value}")
        print("referral from IANA sample:", referral("refer: whois.verisign-grs.com\n"))
        return

    term = args.term or input("Domain or IP: ").strip()
    try:
        text = query(args.server, term)
        if args.server == IANA and not args.raw:
            target = referral(text)
            if target:
                text = query(target, term)
    except OSError as exc:
        raise SystemExit(f"WHOIS error: {exc}")
    if args.raw:
        print(text)
        return
    summary = summarize(text)
    if not summary:
        print("No standard fields found; re-run with --raw to see the full record.")
    for key, values in summary.items():
        for value in values:
            print(f"{key:<22} {value}")

if __name__ == "__main__":
    main()
