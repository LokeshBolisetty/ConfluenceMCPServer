import json
import logging
from .client import Confluence, ConfluenceError

logger = logging.getLogger("confluence_mcp")

# Define content representations
CONTENT_REPRESENTATIONS = {
    "storage": "storage",
    "editor": "editor",
    "view": "view",
    "export_view": "export_view",
    "styled_view": "styled_view"
}

class ManageContent:
    """Class for managing Confluence content."""

    def __init__(self, confluence_client: Confluence):
        self.confluence = confluence_client

    def GetSpaces(self, limit=50):
        """Get all Confluence spaces."""
        try:
            logger.info(f"Fetching up to {limit} Confluence spaces")
            spaces = self.confluence.get_all_spaces(start=0, limit=limit)
            logger.info(f"Successfully retrieved {len(spaces.get('results', []))} spaces")
            # Return the Python object directly instead of JSON string
            return spaces
        except Exception as e:
            logger.error(f"Failed to retrieve spaces: {str(e)}")
            raise ConfluenceError(f"Failed to retrieve spaces: {str(e)}")

    def GetSpaceCount(self):
        """Get count of all active Confluence spaces."""
        spaces = self.confluence.get_all_spaces(start=0, limit=1)
        return spaces.get('size', 0)

    def GetSpace(self, space_key):
        """Get a specific Confluence space by key."""
        space = self.confluence.get_space(space_key)
        return self._remove_null_values(space)

    def GetPagesInSpace(self, space_key, limit=20):
        """Get pages in a specific Confluence space."""
        try:
            pages = self.confluence.get_all_pages_from_space(space_key, start=0, limit=limit)
            return self._get_filtered_pages(pages)
        except Exception as e:
            logger.error(f"Error getting pages for space {space_key}: {str(e)}")
            raise ConfluenceError(f"Error getting pages for space {space_key}: {str(e)}")

    def GetPageCountForSpace(self, space_key):
        """Get count of pages in a specific Confluence space."""
        try:
            # This will return a list of all pages, then we can count them
            pages = self.confluence.get_all_pages_from_space(space_key)
            return len(pages)
        except:
            return 0

    def GetPage(self, page_id):
        """Get a specific Confluence page by ID."""
        try:
            logger.info(f"Fetching Confluence page with ID: {page_id}")
            page = self.confluence.get_page_by_id(page_id, expand='body.storage,version,space,ancestors,descendants.page')
            if not page:
                logger.warning(f"No page found with ID: {page_id}")
                return {"error": f"No page found with ID: {page_id}"}
            logger.info(f"Successfully retrieved page: {page.get('title', 'Untitled')}")
            return self._remove_null_values(page)
        except Exception as e:
            logger.error(f"Error fetching page with ID {page_id}: {str(e)}")
            raise ConfluenceError(f"Error fetching page with ID {page_id}: {str(e)}")

    def GetPageByTitle(self, space_key, title):
        """Get a specific Confluence page by title in a space."""
        page = self.confluence.get_page_by_title(space_key, title, expand='body.storage,version,space,ancestors')
        if page:
            return self._remove_null_values(page)
        return None

    def GetChildPages(self, page_id):
        """Get child pages of a specific Confluence page."""
        try:
            children = self.confluence.get_page_child_by_type(page_id)
            return self._get_filtered_pages(children)
        except Exception as e:
            logger.error(f"Error getting child pages for {page_id}: {str(e)}")
            raise ConfluenceError(f"Error getting child pages for {page_id}: {str(e)}")

    def GetPageAncestors(self, page_id):
        """Get ancestors of a specific Confluence page."""
        try:
            page = self.confluence.get_page_by_id(page_id, expand='ancestors')
            ancestors = page.get('ancestors', []) if page else []
            return self._get_filtered_pages(ancestors)
        except Exception as e:
            logger.error(f"Error getting ancestors for page {page_id}: {str(e)}")
            raise ConfluenceError(f"Error getting ancestors for page {page_id}: {str(e)}")

    def SearchContent(self, query, content_type="page", space_key=None, max_results=10):
        """Search for Confluence content matching a query."""
        try:
            # Clean and escape the query for CQL
            cleaned_query = query.replace('"', '\\"').replace('\\', '\\\\').strip()

            # Construct CQL query
            cql = f'type={content_type} AND text ~ "{cleaned_query}"'
            if space_key:
                cql += f' AND space="{space_key}"'

            logger.info(f"Executing CQL search: {cql} with limit {max_results}")
            results = self.confluence.cql(cql, limit=max_results)

            result_count = len(results.get('results', []))
            logger.info(f"Search returned {result_count} results")

            return self._get_filtered_content(results.get('results', []))
        except Exception as e:
            error_msg = f"Error searching content with query '{query}': {str(e)}"
            logger.error(error_msg)
            raise ConfluenceError(error_msg)

    def GetPageLabels(self, page_id):
        """Get labels for a specific Confluence page."""
        try:
            labels = self.confluence.get_page_labels(page_id)
            return labels
        except Exception as e:
            logger.error(f"Error getting labels for page {page_id}: {str(e)}")
            raise ConfluenceError(f"Error getting labels for page {page_id}: {str(e)}")

    def GetContentByLabel(self, label, space_key=None, content_type="page", max_results=10):
        """Find Confluence content with a specific label."""
        try:
            cql = f'type={content_type} AND label="{label}"'
            if space_key:
                cql += f' AND space="{space_key}"'

            results = self.confluence.cql(cql, limit=max_results)
            return self._get_filtered_content(results.get('results', []))
        except Exception as e:
            logger.error(f"Error getting content with label {label}: {str(e)}")
            raise ConfluenceError(f"Error getting content with label {label}: {str(e)}")

    def GetPageAttachments(self, page_id):
        """Get attachments for a specific Confluence page."""
        try:
            attachments = self.confluence.get_attachments_from_content(page_id)
            return attachments.get('results', [])
        except Exception as e:
            logger.error(f"Error getting attachments for page {page_id}: {str(e)}")
            raise ConfluenceError(f"Error getting attachments for page {page_id}: {str(e)}")

    def _get_filtered_pages(self, pages):
        """Filter pages to include only important fields."""
        filtered_pages = []

        for page in pages:
            filtered_page = {
                'id': page.get('id'),
                'title': page.get('title'),
                'space': page.get('_expandable', {}).get('space') or
                         (page.get('space', {}).get('key') if 'space' in page else None),
                'url': page.get('_links', {}).get('webui')
            }
            filtered_pages.append(filtered_page)

        return filtered_pages

    def _get_filtered_content(self, content_items):
        """Filter content items to include only important fields."""
        filtered_content = []

        for item in content_items:
            filtered_item = {
                'id': item.get('content', {}).get('id') or item.get('id'),
                'title': item.get('content', {}).get('title') or item.get('title'),
                'type': item.get('content', {}).get('type') or item.get('type'),
                'url': item.get('content', {}).get('_links', {}).get('webui') or
                      item.get('_links', {}).get('webui')
            }
            filtered_content.append(filtered_item)

        return filtered_content

    def _remove_null_values(self, obj):
        """Recursively remove null values from dictionaries and lists."""
        if isinstance(obj, dict):
            return {k: self._remove_null_values(v) for k, v in obj.items() if v is not None}
        elif isinstance(obj, list):
            return [self._remove_null_values(item) for item in obj if item is not None]
        else:
            return obj

    def CreatePage(self, space_key, title, body, parent_id=None, representation="storage"):
        """Create a new page in Confluence.

        Args:
            space_key: The key of the space where the page will be created
            title: The title of the new page
            body: The content of the new page (in the specified representation format)
            parent_id: Optional parent page ID if this is a child page
            representation: Content representation - 'storage' for Confluence storage format,
                          'editor' for editor format, etc.

        Returns:
            The created page data if successful
        """
        try:
            logger.info(f"Creating new page '{title}' in space '{space_key}'")

            # Validate the representation type
            if representation not in CONTENT_REPRESENTATIONS:
                representation = "storage"  # Default to storage format

            # Create the page
            if parent_id:
                logger.info(f"Creating as child of page ID: {parent_id}")
                page = self.confluence.create_page(
                    space=space_key,
                    title=title,
                    body=body,
                    parent_id=parent_id,
                    representation=representation
                )
            else:
                page = self.confluence.create_page(
                    space=space_key,
                    title=title,
                    body=body,
                    representation=representation
                )

            logger.info(f"Successfully created page with ID: {page.get('id')}")
            return self._remove_null_values(page)
        except Exception as e:
            error_msg = f"Failed to create page '{title}' in space '{space_key}': {str(e)}"
            logger.error(error_msg)
            raise ConfluenceError(error_msg)

    def UpdatePage(self, page_id, title=None, body=None, representation="storage", version_comment=None):
        """Update an existing Confluence page.

        Args:
            page_id: The ID of the page to update
            title: The new title of the page (optional)
            body: The new content of the page (optional)
            representation: Content representation format
            version_comment: Optional comment for the version history

        Returns:
            The updated page data if successful
        """
        try:
            # Get the current page to get its version number
            current_page = self.confluence.get_page_by_id(page_id)
            if not current_page:
                error_msg = f"Page with ID '{page_id}' not found"
                logger.error(error_msg)
                raise ConfluenceError(error_msg)

            # Extract current version and title if needed
            current_version = current_page.get('version', {}).get('number', 0)
            new_version = current_version + 1
            current_title = current_page.get('title', '')

            # Use current title if none provided
            if not title:
                title = current_title

            # If no body provided, keep existing body
            if not body:
                # Get current body in the requested representation
                body = self.confluence.get_page_by_id(
                    page_id,
                    expand=f"body.{representation}"
                ).get('body', {}).get(representation, {}).get('value', '')

            # Validate the representation type
            if representation not in CONTENT_REPRESENTATIONS:
                representation = "storage"  # Default to storage format

            logger.info(f"Updating page '{title}' (ID: {page_id}) to version {new_version}")

            # Update the page
            # Note: The atlassian-python-api library handles version incrementing automatically
            updated_page = self.confluence.update_page(
                page_id=page_id,
                title=title,
                body=body,
                representation=representation
            )

            # Add version comment if provided
            if version_comment and updated_page:
                self.confluence.set_page_property(
                    page_id=page_id,
                    property_key="version-comment",
                    property_value={"comment": version_comment}
                )
                logger.info(f"Added version comment: {version_comment}")

            logger.info(f"Successfully updated page to version {new_version}")
            return self._remove_null_values(updated_page)
        except Exception as e:
            error_msg = f"Failed to update page '{page_id}': {str(e)}"
            logger.error(error_msg)
            raise ConfluenceError(error_msg)
