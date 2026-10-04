import asyncio
import logging
import urllib.parse
from typing import Dict, List
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from parser import DOMExtractor

# Initialize module-level logger instance matching project-wide log format
logger = logging.getLogger(__name__)


class MDComputersScraper:
    """
    Asynchronous web scraper for MD Computers (https://mdcomputers.in).
    
    Uses Playwright to render JavaScript-heavy e-commerce product listings
    and extracts DOM content for parsing.
    """

    BASE_URL = "https://mdcomputers.in/"

    def __init__(self, headless: bool = True):
        """
        Initialize the scraper instance.

        Args:
            headless (bool): Run browser in headless mode if True, otherwise visible.
        """
        self.headless = headless

    async def fetch_search_results(self, search_term: str) -> List[Dict]:
        """
        Executes search query on MD Computers, captures rendered DOM, and parses results.

        Args:
            search_term (str): Target product query string (e.g., 'external harddrive').

        Returns:
            List[Dict]: List of standardized product records containing details like title, price, status, etc.
        """
        # Encode search term to safely format query string parameters
        encoded_query = urllib.parse.quote_plus(search_term)
        target_url = f"{self.BASE_URL}?route=product/search&search={encoded_query}"

        logger.info(f"Navigating to target URL: {target_url}")

        dom_html = ""

        async with async_playwright() as p:

            # Launch Chromium browser engine with sandbox flags for execution environments
            browser = await p.chromium.launch(
            channel="chrome",
            headless=self.headless,
            )

            # Create isolated browser context with desktop User-Agent
            context = await browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            )

            page = await context.new_page()

            try:
                # Wait for network idle so all dynamic client-side JS elements load
                await page.goto(target_url, wait_until="networkidle", timeout=30000)
                
                # Optional: extra short pause if dynamic content requires extra rendering time
                await page.wait_for_timeout(2000)

                # Capture full client-side rendered (CSR) HTML markup
                dom_html = await page.content()
                logger.info("DOM successfully captured from browser page context.")

            except PlaywrightTimeoutError:
                logger.warning(
                    "Timeout occurred while waiting for page resources to load fully. "
                    "Attempting to capture partial DOM as fallback."
                )
                dom_html = await page.content()
            except Exception as e:
                logger.error(f"Unexpected error encountered during web scraping: {e}", exc_info=True)
            finally:
                # Always close browser context gracefully to release OS processes/memory
                await context.close()
                await browser.close()
                logger.info("Playwright browser instance closed.")

        # Delegate DOM parsing and metadata extraction to parser module
        if dom_html:
            return DOMExtractor.parse_search_results(dom_html, search_term)

        return []