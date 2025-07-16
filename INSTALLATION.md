# Installation Guide for Confluence MCP Server

This guide will help you set up the Confluence MCP Server on your system.

## Prerequisites

- Python 3.8+ installed
- Access to a Confluence Server/DC instance
- Personal Access Token for Confluence authentication

## Step 1: Clone the Repository

If you haven't already, clone the repository containing the Confluence MCP Server:

```bash
git clone <repository-url>
cd <repository-directory>/ConfluenceMCPServer
```

## Step 2: Use Existing Virtual Environment

We'll use the shared virtual environment from the JiraMCPServer project:

```bash
# Activate the existing virtual environment
# On Windows:
..\JiraMCPServer\venv310\Scripts\activate
# On macOS/Linux:
source ../JiraMCPServer/venv310/bin/activate
```

This ensures both MCP servers use the same dependencies and configuration.

## Step 3: Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Step 4: Configure Environment Variables

1. Create a `.env` file in the project root:

```bash
cp .env.example .env
```

2. Edit the `.env` file with your Confluence instance details:

```
CONFLUENCE_URL=https://your-confluence-instance.com
CONFLUENCE_PERSONAL_ACCESS_TOKEN=your_token_here
```

## Step 5: Test the Connection

Before running the server, test that your Confluence connection works:

```bash
python test_connection.py
```

This script will verify if your credentials are correct and if the Confluence API is accessible.

## Step 6: Run the Server

Start the Confluence MCP Server:

```bash
python confluence_mcp_server.py
```

By default, the server will run on http://localhost:8000.

## Step 7: Try the Example Client

To test the functionality, you can use the example client:

```bash
# List spaces
python example_client.py spaces

# Search content
python example_client.py search "your search query"

# Get a specific page
python example_client.py page "page-id"
```

## Step 8: Use the MCP Inspector (Recommended)

The MCP Inspector provides a web interface for testing and debugging the Confluence MCP tools:

```bash
# Start the Confluence MCP server in one terminal
python confluence_mcp_server.py

# Start the MCP Inspector in another terminal
python mcp_inspector.py
```

This will start the inspector on http://localhost:8080 by default. You can then use the web interface to:

- Browse available tools
- Execute tools with different parameters
- View detailed results and errors
- Debug your Confluence integration

## Troubleshooting

- **Connection Issues**: Verify your Confluence URL and token in the `.env` file. Make sure your Confluence instance is accessible from your network.

- **Import Errors**: Ensure all dependencies are installed correctly by running `pip install -r requirements.txt` again.

- **Permission Errors**: Check that your Personal Access Token has sufficient permissions in Confluence to perform the operations you're attempting.

## Next Steps

Once your server is running, you can integrate it with any MCP-compatible client, including AI assistants configured to use MCP tools.
