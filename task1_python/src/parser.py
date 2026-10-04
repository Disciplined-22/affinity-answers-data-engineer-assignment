import datetime
from typing import Dict, List
from bs4 import BeautifulSoup


class DOMExtractor:
    """Parses raw HTML DOM content extracted from MD Computers search results."""

    @staticmethod
    def parse_search_results(html_content: str, search_term: str) -> List[Dict]:
        """
        Parses HTML content to isolate and format product listings.

        Args:
            html_content: Raw HTML text retrieved via Playwright.
            search_term: Target query string used for metadata context.

        Returns:
            List[Dict]: Standardized JSON-like product entries.
        """
        soup = BeautifulSoup(html_content, "html.parser")
        products = []

        # Locate product cards using the provided page layout structure
        items = soup.select(".product-grid-item") or soup.select(".product-wrapper")

        for item in items:
            # Extract product title & item link from product link element
            title_elem = item.select_one(".product-entities-title a") or item.select_one("a.product-image-link")
            
            title = "N/A"
            product_url = "N/A"
            if title_elem:
                # Title might be in the text of .product-entities-title or alt text of the img
                title_text = title_elem.get_text(strip=True)
                if not title_text:
                    img = title_elem.select_one("img")
                    title_text = img.get("alt", "").strip() if img else ""
                
                title = title_text if title_text else "N/A"
                product_url = title_elem.get("href", "N/A")

            # Extract pricing structure (.del for old price, .ins or .amount for new/normal price)
            price_elem = item.select_one(".price")
            normal_price = "N/A"
            special_price = "N/A"

            if price_elem:
                price_del = price_elem.select_one(".del .amount")
                price_ins = price_elem.select_one(".ins .amount")

                if price_del and price_ins:
                    normal_price = price_del.get_text(strip=True)
                    special_price = price_ins.get_text(strip=True)
                elif price_ins:
                    normal_price = price_ins.get_text(strip=True)
                else:
                    amount_elem = price_elem.select_one(".amount")
                    if amount_elem:
                        normal_price = amount_elem.get_text(strip=True)

            # Extract stock availability indicator
            stock_elem = item.select_one(".stock-status") or item.select_one(".stock")
            stock_status = stock_elem.get_text(strip=True) if stock_elem else "In Stock"

            # Construct flexible document payload
            product_doc = {
                "search_term": search_term, # Captures input query to enable traceability and grouping across searches
                "title": title, # Primary product identifier displayed on MD Computers
                "product_url": product_url, # Direct reference link to the product page for validation and deep-linking
                "normal_price": normal_price, # Stores original MRP/list price to maintain historical pricing context
                "special_price": special_price, # Captures discounted/selling price to track active deal values 
                "stock_status": stock_status, # Indicates inventory availability at time of scraping (e.g., In Stock / Out of Stock)
                "scraped_at": datetime.datetime.now(datetime.timezone.utc).isoformat() # ISO UTC timestamp providing metadata for audit trails and other analysis
            }
            products.append(product_doc)

        return products