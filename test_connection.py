#!/usr/bin/env python3
"""
Simple script to test Confluence connection and basic functionality.
Run this to verify your environment setup before starting the MCP server.
"""

import os
import sys
import json
from dotenv import load_dotenv
from atlassian import Confluence
from atlassian.errors import ApiError

def main():
    print("Confluence MCP Server - Connection Test")
    print("=====================================")
    
    # Load environment variables
    load_dotenv()
    url = os.environ.get("CONFLUENCE_URL")
    token = os.environ.get("CONFLUENCE_PERSONAL_ACCESS_TOKEN")
    
    # Check environment variables
    if not url:
        print("ERROR: CONFLUENCE_URL not set in .env file")
        sys.exit(1)
    
    if not token:
        print("ERROR: CONFLUENCE_PERSONAL_ACCESS_TOKEN not set in .env file")
        sys.exit(1)
    
    print(f"Using Confluence URL: {url}")
    print("Attempting to connect...")
    
    try:
        # Create Confluence client
        confluence = Confluence(url=url, token=token)
        
        # Test connection with a simple API call
        # Get the server info instead of user info (which isn't available in this API)
        server_info = confluence.get_all_spaces(limit=1)
        print(f"✅ Connection successful! Connected to Confluence server.")
        
        # Try to get spaces
        spaces = confluence.get_all_spaces(limit=5)
        space_count = len(spaces.get('results', []))
        
        print(f"✅ Successfully retrieved {space_count} spaces")
        if space_count > 0:
            print("\nSpaces found:")
            for space in spaces.get('results', [])[:5]:
                print(f"  - {space.get('name')} ({space.get('key')})")
        
        print("\nYour Confluence connection is correctly configured!")
        print("You can now start the MCP server with: python confluence_mcp_server.py")
        
    except ApiError as e:
        print(f"❌ API Error: {str(e)}")
        print("\nPlease check your URL and Personal Access Token in the .env file.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Connection Error: {str(e)}")
        print("\nPlease check your Confluence server is accessible and credentials are correct.")
        sys.exit(1)

if __name__ == "__main__":
    main()
