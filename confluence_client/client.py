import os
import sys
import logging
from dotenv import load_dotenv
from atlassian import Confluence
from atlassian.errors import ApiError

# Configure logging - use stderr instead of stdout to avoid MCP protocol interference
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger("confluence_mcp")

# Loads variables from .env into the environment
load_dotenv() 

CONFLUENCE_URL = os.environ.get("CONFLUENCE_URL")
CONFLUENCE_PERSONAL_ACCESS_TOKEN = os.environ.get("CONFLUENCE_PERSONAL_ACCESS_TOKEN")

class ConfluenceError(Exception):
    """Custom exception for Confluence client errors."""
    pass

class ConfluenceClient:
    def __init__(self):
        """Instantiate and return a Confluence client."""
        if not CONFLUENCE_URL:
            logger.error("CONFLUENCE_URL environment variable not set")
            raise ConfluenceError("CONFLUENCE_URL environment variable not set")
        
        if not CONFLUENCE_PERSONAL_ACCESS_TOKEN:
            logger.error("CONFLUENCE_PERSONAL_ACCESS_TOKEN environment variable not set")
            raise ConfluenceError("CONFLUENCE_PERSONAL_ACCESS_TOKEN environment variable not set")
            
        try:
            logger.info(f"Connecting to Confluence at {CONFLUENCE_URL}")
            self.client = Confluence(
                url=CONFLUENCE_URL,
                token=CONFLUENCE_PERSONAL_ACCESS_TOKEN
            )
            # Test the connection
            self._test_connection()
            logger.info("Successfully connected to Confluence")
        except Exception as e:
            logger.error(f"Failed to connect to Confluence: {str(e)}")
            raise ConfluenceError(f"Failed to connect to Confluence: {str(e)}")
    
    def _test_connection(self):
        """Test the Confluence connection."""
        try:
            # Try to get space information - a simple API call to test authentication
            # This is available in the Confluence API (unlike get_current_user)
            self.client.get_all_spaces(start=0, limit=1)
            logger.info("Connection test successful")
        except ApiError as e:
            logger.error(f"API Error: {str(e)}")
            raise ConfluenceError(f"API Error: {str(e)}")
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            raise ConfluenceError(f"Connection test failed: {str(e)}")
