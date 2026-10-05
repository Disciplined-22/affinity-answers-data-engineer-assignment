## Design Choices for Question 1: Python

* **Playwright:** Used Playwright over HTTP requests because it is easier and faster to implement, while also providing better support for future authentication and bot-detection requirements.

* **MongoDB:** Used MongoDB because of its flexible schema, making it easier to handle website structure changes and capture varying product data; it also supports horizontal scaling (SQL databases may require additional operational overhead for horizontal scaling).

## Output Format choice

```json
Example
{
  "search_term": "external harddrive",  # Captures input query to enable traceability and grouping across searches
  "title": "Seagate Expansion 1TB External Hard Drive", # Primary product identifier displayed on MD Computers
  "product_url": "product_url_present_in_website", # Direct reference link to the product page for validation and deep-linking
  "normal_price": "₹10,000", # Stores original MRP/list price to maintain historical pricing context
  "special_price": "₹9,699", # Captures discounted/selling price to track active deal values
  "stock_status": "In Stock", # Indicates inventory availability at time of scraping (e.g., In Stock / Out of Stock)
  "scraped_at": "2026-03-30T10:15:30.123456+00:00"  # ISO UTC timestamp providing metadata for audit trails and other analysis
}

```

<!-- Note : You need  to have an .env file(and it has not been pushed here ) in that mention your mongo url in the variable MONGO_URI -->

```json
MONGO_URI=""
```