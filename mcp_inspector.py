#!/usr/bin/env python3
"""
MCP Inspector for Confluence MCP Server
This provides a web-based interface to test and debug the Confluence MCP tools.
"""

import sys
import os
import argparse
from mcp.inspector import run_inspector

# Add the parent directory to sys.path to allow importing from the Confluence module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    parser = argparse.ArgumentParser(description='MCP Inspector for Confluence MCP Server')
    parser.add_argument('--host', default='localhost', help='Host to run the inspector on')
    parser.add_argument('--port', type=int, default=8080, help='Port to run the inspector on')
    parser.add_argument('--server-url', default='http://localhost:8000', help='URL of the running MCP server')
    
    args = parser.parse_args()
    
    print(f"Starting MCP Inspector for Confluence...")
    print(f"Inspector URL: http://{args.host}:{args.port}")
    print(f"Connecting to MCP server at: {args.server_url}")
    print("Use Ctrl+C to stop the inspector")
    
    run_inspector(
        server_url=args.server_url,
        host=args.host,
        port=args.port
    )

if __name__ == '__main__':
    main()
