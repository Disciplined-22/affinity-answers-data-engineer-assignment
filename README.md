## Design Choices for Question 1: Python

- **Playwright:** Used Playwright over HTTP requests because it is easier and faster to implement, while also providing better support for future authentication and bot-detection requirements.
- **MongoDB:** Used MongoDB because of its flexible schema, making it easier to handle website structure changes and capture varying product data; it also supports horizontal scaling (SQL databases may require additional operational overhead for horizontal scaling).

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



## Environment Setup & Execution



### 1. Install Dependencies & Activate Virtual Environment

Create and Activate your virtual environment (`.venv`):

```bash
python -m venv .venv

# On Linux/macOS
source .venv/bin/activate

# On Windows (PowerShell)
.venv\Scripts\Activate.ps1

# On Windows (CMD)
.venv\Scripts\activate.bat
```

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```



### 2. Configure Environment Variables

Create a .env file in the root directory and define your MongoDB URI:

```bash
MONGO_URI="mongodb+srv://<username>:<password>@cluster.mongodb.net/dbname?retryWrites=true&w=majority"
```



### 3. Run the Scraper

```bash
python task1_python/src/main.py "external harddrive"
```



## SQL Execution & Query Setup (Task 2)

All queries for Task 2 are stored in individual `.sql` files inside the `task2_sql` directory:

1. `task2_sql/query1_acacia.sql`
2. `task2_sql/query2_wheat.sql`
3. `task2_sql/query3_pagination.sql`

---



### Execution Instructions

To execute these queries:

1. Open your database management tool or MySQL client (e.g., **DBeaver**, **MySQL Workbench**, or the command-line interface).
2. Connect to your active **MySQL** database server.
3. Open each SQL file directly from the `task2_sql/` directory, or copy the query contents into an active SQL editor tab.
4. Execute each statement sequentially against the database.



## Environment Setup & Execution (Task 3)



### 1. Build and Start Docker Services

Spin up the required services using Docker Compose: (I am using Windows, so I need to use Docker for a Linux environment.)

```bash
docker compose up -d --build
```



### 2. Make Shell Script Executable

Grant execution permissions to the shell script: (need to run inside docker terminal)

```bash
chmod +x task3_shell/extract_companies.sh
```



### 3. Run the Script

Execute the shell script by passing the dataset URL as an argument: (need to run inside docker terminal)

```bash 
./task3_shell/extract_companies.sh "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/refs/heads/main/data/constituents.csv"
```

