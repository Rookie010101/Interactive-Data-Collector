# 📚 Bookstore Inventory Management & Sales Analysis

A structured dataset system for managing bookstore inventory and tracking sales performance across titles, genres, and time periods.

---

## 📁 Project Structure

```
bookstore/
├── README.md                  # Project documentation
├── bookstore_inventory.csv    # Master inventory dataset
└── sales.csv                  # Sales transactions dataset
```

---

## 📊 Datasets

### 1. `bookstore_inventory.csv`

The master inventory file containing all books available in the store.

| Column     | Type    | Description                        | Example                  |
|------------|---------|------------------------------------|--------------------------|
| `Title`    | String  | Full title of the book             | The Great Gatsby         |
| `Author`   | String  | Full name of the author            | F. Scott Fitzgerald      |
| `Genre`    | String  | Book genre/category                | Classic Fiction          |
| `Price`    | Float   | Retail price in USD                | 12.99                    |
| `Quantity` | Integer | Current stock count                | 45                       |

**Dataset Summary:**
- Total Records: **60 books**
- Price Range: **$7.99 – $22.99**
- Stock Range: **18 – 90 units**
- Genres Covered: **15 genres**

**Genres Available:**

| Genre                 | Genre               |
|-----------------------|---------------------|
| Classic Fiction       | Non-Fiction         |
| Dystopian Fiction     | Psychology          |
| Literary Fiction      | Self-Help           |
| Fantasy               | Biography           |
| Science Fiction       | Philosophical Fiction |
| Thriller              | Children's          |
| Mystery               | Young Adult         |
| Romance               |                     |

---

### 2. `sales.csv`

Transaction-level sales data tracking daily book sales with revenue.

| Column           | Type    | Description                          | Example       |
|------------------|---------|--------------------------------------|---------------|
| `Date`           | Date    | Transaction date (YYYY-MM-DD format) | 2024-01-03    |
| `Title`          | String  | Title of the book sold               | Atomic Habits |
| `Quantity Sold`  | Integer | Number of units sold                 | 5             |
| `Total Revenue`  | Float   | Revenue generated (USD)              | 84.95         |

**Dataset Summary:**
- Total Records: **120 transactions**
- Date Range: **January 2024 – June 2024**
- Quantity Sold per Transaction: **2 – 10 units**
- Revenue is calculated as: `Quantity Sold × Unit Price`

---

## 🔗 Dataset Relationships

The two datasets are linked via the `Title` column and can be joined for deeper analysis:

```
bookstore_inventory.csv          sales.csv
─────────────────────            ─────────────────
Title  ◄────────────────────────  Title
Author                            Date
Genre                             Quantity Sold
Price  ──────────────────────────► Total Revenue (Price × Quantity Sold)
Quantity
```

---

## 📈 Possible Analyses

### Inventory Analysis
- Identify **low-stock books** that need restocking (`Quantity < 25`)
- Find the **most expensive** and **most affordable** books
- Breakdown of **inventory by genre**
- Calculate **total inventory value** (`Price × Quantity`)

### Sales Analysis
- Track **monthly revenue trends** over Jan–Jun 2024
- Identify **best-selling titles** by quantity sold
- Find **top revenue-generating books**
- Analyze **sales by genre** (via join with inventory)
- Calculate **average order value** per transaction

### Combined / Advanced Analysis
- Compare **stock levels vs. sales velocity** to flag reorder needs
- Identify **slow-moving inventory** (high stock, low sales)
- Compute **sell-through rate**: `Total Units Sold / Starting Quantity`
- **Author performance**: total revenue grouped by author

---

## 🛠️ Usage Examples

### Python (pandas)

```python
import pandas as pd

# Load datasets
inventory = pd.read_csv("bookstore_inventory.csv")
sales = pd.read_csv("sales.csv", parse_dates=["Date"])

# Total inventory value
inventory["Stock Value"] = inventory["Price"] * inventory["Quantity"]
print(f"Total Inventory Value: ${inventory['Stock Value'].sum():,.2f}")

# Monthly revenue
sales["Month"] = sales["Date"].dt.to_period("M")
monthly_revenue = sales.groupby("Month")["Total Revenue"].sum()
print(monthly_revenue)

# Top 5 best-selling titles
top_sellers = (
    sales.groupby("Title")["Quantity Sold"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)
print(top_sellers)

# Join datasets
merged = sales.merge(inventory[["Title", "Author", "Genre", "Price"]], on="Title")
genre_revenue = merged.groupby("Genre")["Total Revenue"].sum().sort_values(ascending=False)
print(genre_revenue)
```

### SQL

```sql
-- Top 5 revenue-generating books
SELECT Title, SUM("Total Revenue") AS total_revenue
FROM sales
GROUP BY Title
ORDER BY total_revenue DESC
LIMIT 5;

-- Low stock alert
SELECT Title, Author, Genre, Quantity
FROM bookstore_inventory
WHERE Quantity < 25
ORDER BY Quantity ASC;

-- Monthly revenue trend
SELECT strftime('%Y-%m', Date) AS month, SUM("Total Revenue") AS revenue
FROM sales
GROUP BY month
ORDER BY month;

-- Genre-wise sales performance
SELECT i.Genre, COUNT(*) AS transactions, SUM(s."Quantity Sold") AS units_sold,
       ROUND(SUM(s."Total Revenue"), 2) AS total_revenue
FROM sales s
JOIN bookstore_inventory i ON s.Title = i.Title
GROUP BY i.Genre
ORDER BY total_revenue DESC;
```

---

## 📋 Data Quality Notes

- All `Total Revenue` values in `sales.csv` are consistent with `Price × Quantity Sold` from the inventory.
- All titles in `sales.csv` exist in `bookstore_inventory.csv` — safe to join on `Title`.
- Dates follow ISO 8601 format (`YYYY-MM-DD`) for easy parsing in all tools.
- No null or missing values in either dataset.
- Prices use 2 decimal places (USD).

---

## 🚀 Getting Started

1. Clone or download the project folder.
2. Ensure both CSV files are in the same directory.
3. Open with your preferred tool:
   - **Python**: `pandas`, `matplotlib`, `seaborn`
   - **Excel / Google Sheets**: Import CSV directly
   - **SQL**: Load into SQLite, PostgreSQL, or DuckDB
   - **BI Tools**: Tableau, Power BI, Metabase

---

## 📌 Notes

- Prices are in **USD**.
- Inventory quantities represent **current stock levels** at the time of dataset creation.
- Sales data covers **H1 2024** (January through June).
- This dataset is intended for **educational, analytical, and prototyping** purposes.

---

*Generated for Bookstore Inventory Management & Sales Analysis Project*
