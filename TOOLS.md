# Confluence MCP Server Tools

This document describes the tools available in the Confluence MCP Server for AI assistants to interact with Confluence content.

## Content Creation and Modification Tools

### `create_page(space_key, title, body, parent_id=None, representation="storage")`

Creates a new page in Confluence.

**Parameters:**
- `space_key`: The key of the space where the page will be created.
- `title`: The title of the new page.
- `body`: The content of the new page.
- `parent_id`: (Optional) Parent page ID if this is a child page.
- `representation`: (Optional) Content representation format (default: "storage").

**Returns:** The created page data including ID, title, version, etc.

**Example:**
```python
# Create a simple page
create_page(
    space_key="DOC", 
    title="New Documentation", 
    body="<p>This is a new page created via the Confluence MCP Server.</p>"
)

# Create a child page under a parent
create_page(
    space_key="DOC", 
    title="Child Page", 
    body="<p>This is a child page.</p>",
    parent_id="12345678"
)
```

### `update_page(page_id, title=None, body=None, representation="storage", version_comment=None)`

Updates an existing Confluence page.

**Parameters:**
- `page_id`: The ID of the page to update.
- `title`: (Optional) The new title of the page.
- `body`: (Optional) The new content of the page.
- `representation`: (Optional) Content representation format (default: "storage").
- `version_comment`: (Optional) Comment for the version history.

**Returns:** The updated page data including ID, title, version, etc.

**Example:**
```python
# Update page content only
update_page(
    page_id="12345678", 
    body="<p>Updated content for this page.</p>",
    version_comment="Updated via API"
)

# Update both title and content
update_page(
    page_id="12345678", 
    title="New Page Title",
    body="<p>Completely revised content.</p>"
)
```

## Content Query Tools

### `get_spaces()`

Retrieves all available Confluence spaces.

**Returns:** List of space dictionaries with keys like id, key, name, type, etc.

### `get_space_count()`

Retrieves the count of all active Confluence spaces.

**Returns:** Integer count of spaces.

### `get_space(space_key)`

Retrieves details for a specific Confluence space.

**Parameters:**
- `space_key`: The key of the Confluence space.

**Returns:** Space details dictionary.

### `get_pages_in_space(space_key, limit=20)`

Retrieves pages from a specific Confluence space.

**Parameters:**
- `space_key`: The key of the Confluence space.
- `limit`: Maximum number of pages to return (default: 20).

**Returns:** List of page dictionaries.

### `get_page_count_for_space(space_key)`

Retrieves the count of pages for a specific Confluence space.

**Parameters:**
- `space_key`: The key of the Confluence space.

**Returns:** Integer count of pages.

### `get_page(page_id)`

Retrieves details of a specific Confluence page.

**Parameters:**
- `page_id`: The ID of the Confluence page.

**Returns:** Page details including content.

### `get_page_by_title(space_key, title)`

Retrieves a page by its title in a specific space.

**Parameters:**
- `space_key`: The key of the Confluence space.
- `title`: The title of the page to find.

**Returns:** Page details including content, or None if not found.

### `get_child_pages(page_id)`

Retrieves child pages of a specific Confluence page.

**Parameters:**
- `page_id`: The ID of the parent Confluence page.

**Returns:** List of child page dictionaries.

### `get_page_ancestors(page_id)`

Retrieves ancestors of a specific Confluence page.

**Parameters:**
- `page_id`: The ID of the Confluence page.

**Returns:** List of ancestor page dictionaries.

### `search_content(query, content_type="page", space_key=None, max_results=10)`

Searches for Confluence content matching a query.

**Parameters:**
- `query`: The text to search for.
- `content_type`: The type of content to search for (default: "page").
- `space_key`: Optional space key to restrict search to.
- `max_results`: Maximum number of results to return (default: 10).

**Returns:** List of matching content items.

### `get_page_labels(page_id)`

Retrieves labels for a specific Confluence page.

**Parameters:**
- `page_id`: The ID of the Confluence page.

**Returns:** List of label dictionaries.

### `get_content_by_label(label, space_key=None, content_type="page", max_results=10)`

Finds Confluence content with a specific label.

**Parameters:**
- `label`: The label to search for.
- `space_key`: Optional space key to restrict search to.
- `content_type`: The type of content to search for (default: "page").
- `max_results`: Maximum number of results to return (default: 10).

**Returns:** List of content items with the specified label.

### `get_page_attachments(page_id)`

Retrieves attachments for a specific Confluence page.

**Parameters:**
- `page_id`: The ID of the Confluence page.

**Returns:** List of attachment dictionaries.

## Example Tool

### `add(a, b)`

Adds two numbers and returns the result.

**Parameters:**
- `a`: First integer.
- `b`: Second integer.

**Returns:** The sum of a and b.
