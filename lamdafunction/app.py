# lambda_function.py
import json
import logging
import nest_asyncio
from scrapegraphai.graphs import SmartScraperGraph

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Apply nest_asyncio to prevent event loop conflicts
nest_asyncio.apply()

# Configuration for SmartScraperGraph
GRAPH_CONFIG = {
    "llm": {
        "model": "ollama/mistral",
        "temperature": 0,
        "format": "json",
        "base_url": "http://localhost:11434",
        "max_tokens": 1024,
        "chunk_size": 512,
        "chunk_overlap": 50
    },
    "embeddings": {
        "model": "ollama/nomic-embed-text",
        "base_url": "http://localhost:11434",
    },
    "scraping": {
        "max_depth": 2,
        "max_pages": 10,
        "timeout": 30
    }
}

def validate_input(body):
    """Validate the input parameters."""
    if not body.get("url"):
        raise ValueError("URL is required")
    if not isinstance(body.get("url"), str):
        raise ValueError("URL must be a string")
    if body.get("prompt") and not isinstance(body.get("prompt"), str):
        raise ValueError("Prompt must be a string if provided")

def format_response(status_code, body):
    """Format the API Gateway response."""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",  # Enable CORS
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "POST, OPTIONS"
        },
        "body": json.dumps(body)
    }

class SmartScraper:
    def __init__(self, prompt, source, config):
        self.prompt = prompt
        self.source = source
        self.config = config
        self.graph = SmartScraperGraph(
            prompt=prompt,
            source=source,
            config=config
        )

    def run(self):
        """Execute the scraping operation."""
        try:
            logger.info(f"Starting scraping of {self.source}")
            result = self.graph.run()
            return result
        except Exception as e:
            logger.error(f"Error during scraping: {e}")
            raise

def lambda_handler(event, context):
    """AWS Lambda handler function."""
    logger.info("Received event: %s", json.dumps(event))
    
    # Handle OPTIONS request for CORS
    if event.get("httpMethod") == "OPTIONS":
        return format_response(200, {"message": "CORS enabled"})
    
    try:
        # Parse the request body
        body = json.loads(event.get("body", "{}"))
        
        # Validate input
        try:
            validate_input(body)
        except ValueError as e:
            return format_response(400, {"error": str(e)})
        
        # Extract parameters
        url = body.get("url")
        prompt = body.get("prompt", "What is this about?")
        
        # Initialize scraper with custom configuration
        config = GRAPH_CONFIG.copy()
        if body.get("max_depth"):
            config["scraping"]["max_depth"] = int(body["max_depth"])
        if body.get("max_pages"):
            config["scraping"]["max_pages"] = int(body["max_pages"])
            
        # Execute scraping
        scraper = SmartScraper(prompt=prompt, source=url, config=config)
        result = scraper.run()
        
        # Return success response
        return format_response(200, {
            "status": "success",
            "data": result,
            "metadata": {
                "url": url,
                "prompt": prompt
            }
        })
        
    except json.JSONDecodeError:
        return format_response(400, {"error": "Invalid JSON in request body"})
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return format_response(500, {"error": f"Internal server error: {str(e)}"})
