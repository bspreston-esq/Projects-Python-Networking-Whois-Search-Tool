# Whois Search Tool

**Category:** Networking

## Problem

Enter an IP or host address and have it look it up through whois and return the results to you.

## Solution

Speaks the WHOIS protocol directly over TCP port 43: asks IANA for the authoritative server, follows the `refer:` line, then extracts common fields (registrar, dates, name servers, status). `--raw` prints the untouched record; the demo summarizes an embedded sample offline.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py example.com
python3 main.py 8.8.8.8 --server whois.arin.net
python3 main.py --demo
```

## Example

```text
domain name            EXAMPLE.COM
registrar              RESERVED-Internet Assigned Numbers Authority
creation date          1995-08-14T04:00:00Z
registry expiry date   2025-08-13T04:00:00Z
name server            A.IANA-SERVERS.NET
name server            B.IANA-SERVERS.NET
```

## Attribution

The problem statement is from [karan/Projects](https://github.com/karan/Projects), a list of practical projects that anyone can solve in any programming language (MIT License, Copyright (c) 2013 Karan Goel). The Python solution in this repository was implemented by [bspreston-esq](https://github.com/bspreston-esq).

This repository is part of the [Projects-Python-All](https://github.com/bspreston-esq/Projects-Python-All) collection.
