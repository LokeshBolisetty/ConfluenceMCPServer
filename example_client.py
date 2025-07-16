#!/usr/bin/env python3
"""
Example MCP Client for Confluence MCP Server
This demonstrates how to connect to the Confluence MCP Server and use its tools.
"""

import argparse
import json
import sys
from mcp.client import Client
from mcp.rpc import RpcError

def format_output(data):
    """Format output for better readability."""
    if isinstance(data, str):
        try:
            # Try to parse as JSON for prettier printing
            parsed_data = json.loads(data)
            return json.dumps(parsed_data, indent=2)
        except:
            # If not JSON, return as is
            return data
    return json.dumps(data, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Example client for Confluence MCP Server')
    parser.add_argument('--host', default='localhost', help='MCP server hostname')
    parser.add_argument('--port', type=int, default=8000, help='MCP server port')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add two numbers')
    add_parser.add_argument('a', type=int, help='First number')
    add_parser.add_argument('b', type=int, help='Second number')
    
    # Get spaces command
    spaces_parser = subparsers.add_parser('spaces', help='Get Confluence spaces')
    spaces_parser.add_argument('--limit', type=int, default=20, help='Max spaces to return')
    
    # Get space command
    space_parser = subparsers.add_parser('space', help='Get a specific Confluence space')
    space_parser.add_argument('key', help='Space key')
    
    # Get pages in space command
    pages_parser = subparsers.add_parser('pages', help='Get pages in a Confluence space')
    pages_parser.add_argument('space_key', help='Space key')
    pages_parser.add_argument('--limit', type=int, default=20, help='Max pages to return')
    
    # Get page command
    page_parser = subparsers.add_parser('page', help='Get a specific Confluence page')
    page_parser.add_argument('page_id', help='Page ID')
    
    # Search content command
    search_parser = subparsers.add_parser('search', help='Search Confluence content')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--space', help='Space key to limit search to')
    search_parser.add_argument('--type', default='page', help='Content type (default: page)')
    search_parser.add_argument('--limit', type=int, default=10, help='Max results to return')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Connect to the MCP server
    try:
        client = Client(f'http://{args.host}:{args.port}')
        print(f"Connected to Confluence MCP Server at http://{args.host}:{args.port}")
        
        # Execute the requested command
        result = None
        if args.command == 'add':
            result = client.add(a=args.a, b=args.b)
            print(f"Result: {result}")
            
        elif args.command == 'spaces':
            result = client.get_spaces(limit=args.limit)
            print(format_output(result))
            
        elif args.command == 'space':
            result = client.get_space(space_key=args.key)
            print(format_output(result))
            
        elif args.command == 'pages':
            result = client.get_pages_in_space(space_key=args.space_key, limit=args.limit)
            print(format_output(result))
            
        elif args.command == 'page':
            result = client.get_page(page_id=args.page_id)
            print(format_output(result))
            
        elif args.command == 'search':
            result = client.search_content(
                query=args.query, 
                content_type=args.type, 
                space_key=args.space, 
                max_results=args.limit
            )
            print(format_output(result))
            
    except RpcError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
