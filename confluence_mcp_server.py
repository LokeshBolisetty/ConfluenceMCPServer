import sys
import logging
from mcp.server.fastmcp import FastMCP
from confluence_client import ConfluenceClient, ManageContent
from confluence_client.client import ConfluenceError
from typing import List, Dict, Optional, Union

# Configure logging - use stderr instead of stdout to avoid MCP protocol interference
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger("confluence_mcp_server")

# Instantiate the MCP server
mcp = FastMCP("Confluence")

# Instantiate Confluence management classes
try:
    logger.info("Initializing Confluence client...")
    confluence_client = ConfluenceClient().client
    manage_content = ManageContent(confluence_client)
    logger.info("Confluence MCP server initialization successful")
except ConfluenceError as e:
    logger.error(f"Failed to initialize Confluence client: {e}")
    sys.exit(1)
except Exception as e:
    logger.error(f"Unexpected error during initialization: {e}")
    sys.exit(1)

# Example tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers and return the result."""
    return a + b

# Content Management Tools

# Content Creation and Modification Tools
@mcp.tool()
def create_page(space_key: str, title: str, body: str, parent_id: Optional[str] = None, representation: str = "storage") -> Dict:
    """
    Create a new page in Confluence.
    Args:
        space_key: The key of the space where the page will be created
        title: The title of the new page
        body: The content of the new page
        parent_id: Optional parent page ID if this is a child page
        representation: Content representation format (default: "storage")
    Returns:
        The created page data
    """
    return manage_content.CreatePage(space_key, title, body, parent_id, representation)

@mcp.tool()
def update_page(page_id: str, title: str = None, body: str = None, representation: str = "storage", version_comment: str = None) -> Dict:
    """
    Update an existing Confluence page.
    Args:
        page_id: The ID of the page to update
        title: The new title of the page (optional)
        body: The new content of the page (optional)
        representation: Content representation format (default: "storage")
        version_comment: Optional comment for the version history
    Returns:
        The updated page data
    """
    return manage_content.UpdatePage(page_id, title, body, representation, version_comment)

# Content Query Tools
@mcp.tool()
def get_spaces(limit: int = 50) -> str:
    """
    Retrieve all available Confluence spaces.
    Args:
        limit: Maximum number of spaces to return.
    Returns:
        List of space dictionaries.
    """
    return manage_content.GetSpaces(limit)

@mcp.tool()
def get_space_count() -> int:
    """
    Retrieve the count of all active Confluence spaces.
    Returns:
        Integer count of spaces.
    """
    return manage_content.GetSpaceCount()

@mcp.tool()
def get_space(space_key: str) -> Dict:
    """
    Retrieve details for a specific Confluence space.
    Args:
        space_key: The key of the Confluence space.
    Returns:
        Space details dictionary.
    """
    return manage_content.GetSpace(space_key)

@mcp.tool()
def get_pages_in_space(space_key: str, limit: int = 20) -> str:
    """
    Retrieve pages from a specific Confluence space.
    Args:
        space_key: The key of the Confluence space.
        limit: Maximum number of pages to return.
    Returns:
        List of page dictionaries.
    """
    return manage_content.GetPagesInSpace(space_key, limit)

@mcp.tool()
def get_page_count_for_space(space_key: str) -> int:
    """
    Retrieve the count of pages for a specific Confluence space.
    Args:
        space_key: The key of the Confluence space.
    Returns:
        Integer count of pages.
    """
    return manage_content.GetPageCountForSpace(space_key)

@mcp.tool()
def get_page(page_id: str) -> Dict:
    """
    Retrieve details of a specific Confluence page.
    Args:
        page_id: The ID of the Confluence page.
    Returns:
        Page details including content.
    """
    return manage_content.GetPage(page_id)

@mcp.tool()
def get_page_by_title(space_key: str, title: str) -> Optional[Dict]:
    """
    Retrieve a page by its title in a specific space.
    Args:
        space_key: The key of the Confluence space.
        title: The title of the page to find.
    Returns:
        Page details including content, or None if not found.
    """
    return manage_content.GetPageByTitle(space_key, title)

@mcp.tool()
def get_child_pages(page_id: str) -> str:
    """
    Retrieve child pages of a specific Confluence page.
    Args:
        page_id: The ID of the parent Confluence page.
    Returns:
        List of child page dictionaries.
    """
    return manage_content.GetChildPages(page_id)

@mcp.tool()
def get_page_ancestors(page_id: str) -> str:
    """
    Retrieve ancestors of a specific Confluence page.
    Args:
        page_id: The ID of the Confluence page.
    Returns:
        List of ancestor page dictionaries.
    """
    return manage_content.GetPageAncestors(page_id)

@mcp.tool()
def search_content(query: str, content_type: str = "page", space_key: Optional[str] = None, max_results: int = 10) -> str:
    """
    Search for Confluence content matching a query.
    Args:
        query: The text to search for.
        content_type: The type of content to search for (default: "page").
        space_key: Optional space key to restrict search to.
        max_results: Maximum number of results to return (default: 10).
    Returns:
        List of matching content items.
    """
    return manage_content.SearchContent(query, content_type, space_key, max_results)

@mcp.tool()
def get_page_labels(page_id: str) -> str:
    """
    Retrieve labels for a specific Confluence page.
    Args:
        page_id: The ID of the Confluence page.
    Returns:
        List of label dictionaries.
    """
    return manage_content.GetPageLabels(page_id)

@mcp.tool()
def get_content_by_label(label: str, space_key: Optional[str] = None, content_type: str = "page", max_results: int = 10) -> str:
    """
    Find Confluence content with a specific label.
    Args:
        label: The label to search for.
        space_key: Optional space key to restrict search to.
        content_type: The type of content to search for (default: "page").
        max_results: Maximum number of results to return (default: 10).
    Returns:
        List of content items with the specified label.
    """
    return manage_content.GetContentByLabel(label, space_key, content_type, max_results)

@mcp.tool()
def get_page_attachments(page_id: str) -> str:
    """
    Retrieve attachments for a specific Confluence page.
    Args:
        page_id: The ID of the Confluence page.
    Returns:
        List of attachment dictionaries.
    """
    return manage_content.GetPageAttachments(page_id)

if __name__ == "__main__":
    mcp.run()
