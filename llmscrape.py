import nest_asyncio
from scrapegraphai.graphs import SmartScraperGraph
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Apply nest_asyncio to prevent event loop conflicts
nest_asyncio.apply()

# Configuration for SmartScraperGraph with chunking parameters
graph_config = {
    "llm": {
        "model": "ollama/mistral",
        "temperature": 0,
        "format": "json",
        "base_url": "http://localhost:11434",
        "max_tokens": 1024,  # Limit token length
        "chunk_size": 512,   # Size of chunks to process
        "chunk_overlap": 50  # Overlap between chunks
    },
    "embeddings": {
        "model": "ollama/nomic-embed-text",
        "base_url": "http://localhost:11434",
    },
    "scraping": {
        "max_depth": 2,      # Limit scraping depth
        "max_pages": 10,     # Limit number of pages
        "timeout": 30        # Request timeout in seconds
    }
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
    
    def chunk_text(self, text, chunk_size=512):
        """Split text into smaller chunks to avoid token length issues."""
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
        return chunks
    
    def run(self):
        try:
            logger.info(f"Starting scraping of {self.source}")
            result = self.graph.run()
            return result
        except Exception as e:
            logger.error(f"Error during scraping: {e}")
            return None

def run_smart_scraper():
    try:
        scraper = SmartScraper(
            prompt="What is this about?",
            source="https://dev.to/t/webdev",
            config=graph_config
        )
        result = scraper.run()
        
        if result:
            logger.info("Scraping completed successfully")
            print(result)
        else:
            logger.error("Scraping failed to produce results")
            
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    run_smart_scraper()