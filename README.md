# Confluence MCP Server

A Model Context Protocol (MCP) server for Atlassian Confluence that allows AI assistants to interact with Confluence content.

## Overview

This server implements the Model Context Protocol (MCP) for interacting with Confluence Server/DC data. It enables AI models to query and work with Confluence spaces, pages, and content through well-defined tools.

## Features

- Query Confluence spaces and pages
- Retrieve content by ID or title
- Search for content across spaces
- View content metadata and properties
- Navigate page hierarchies and relationships

## Requirements

- Confluence Server/DC instance
- Personal Access Token for authentication
- Python 3.8+

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root with the following variables:
   ```
   CONFLUENCE_URL=https://your-confluence-instance.com
   CONFLUENCE_PERSONAL_ACCESS_TOKEN=your_token_here
   ```

## Usage

1. Start the server:
   ```
   python confluence_mcp_server.py
   ```

2. Use an MCP client to connect to the server and invoke the available tools.

## Tools

See the [TOOLS.md](TOOLS.md) file for detailed documentation of all available tools.

## Architecture

- **confluence_mcp_server.py**: Main server implementation
- **confluence_client/**: Client modules for Confluence API
- **models/**: Data models and schemas

## License

This project is licensed under the MIT License.
