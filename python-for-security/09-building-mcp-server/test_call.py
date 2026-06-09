#!/usr/bin/env python3
"""
Simple MCP client that calls the enrich_ip tool directly (without stdio transport).
Used by make demo and for student testing.
"""

import importlib
import json
import sys


def main() -> None:
    """Call server.enrich_ip() directly and print the result."""
    # Import the server module so we can call the tool function directly.
    # In a real MCP client, this would go over stdio; for lab testing, direct import is sufficient.
    import server

    if len(sys.argv) < 3:
        print("Usage: python test_call.py enrich_ip '{\"ip\": \"8.8.8.8\"}'")
        sys.exit(1)

    tool_name = sys.argv[1]
    args = json.loads(sys.argv[2])

    if tool_name == "enrich_ip":
        result = server.enrich_ip(**args)
    else:
        print(f"Unknown tool: {tool_name}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
