# product_catalog.py
# Day 10 AM - E-Commerce Product Catalog System

from collections import defaultdict

# ─────────────────────────────────────────
# Product Catalog — nested dicts
# ─────────────────────────────────────────
catalog = {
    "SKU001": {"name": "Laptop",          "price": 65000, "category": "electronics", "stock": 15, "rating": 4.5, "tags": ["computer", "work", "portable"]},
    "SKU002": {"name": "Smartphone",      "price": 45000, "category": "electronics", "stock": 20, "rating": 4.3, "tags": ["mobile", "work", "portable"]},
    "SKU003": {"name": "Bluetooth Speaker","price": 3500,  "category": "electronics", "stock": 0,  "rating": 4.1, "tags": ["audio", "portable", "music"]},
    "SKU004": {"name": "Smartwatch",      "price": 12000, "category": "electronics", "stock": 8,  "rating": 4.0, "tags": ["wearable", "fitness", "portable"]},
    "SKU005": {"name": "Headphones",      "price": 8000,  "category": "electronics", "stock": 12, "rating": 4.6, "tags": ["audio", "music", "work"]},
    "SKU006": {"name": "T-Shirt",         "price": 799,   "category": "clothing",    "stock": 50, "rating": 3.9, "tags": ["casual", "summer", "cotton"]},
    "SKU007": {"name": "Jeans",           "price": 1499,  "category": "clothing",    "stock": 30, "rating": 4.0, "tags": ["casual", "denim", "fashion"]},
    "SKU008": {"name": "Jacket",          "price": 2999,  "category": "clothing",    "stock": 0,  "rating": 4.2, "tags": ["winter", "fashion", "outdoor"]},
    "SKU009": {"name": "Sneakers",        "price": 3499,  "category": "clothing",    "stock": 25, "rating": 4.4, "tags": ["footwear", "casual", "sports"]},
    "SKU010": {"name": "Clean Code",      "price": 599,   "category": "books",       "stock": 40, "rating": 4.8, "tags": ["programming", "software", "education"]},
    "SKU011": {"name": "Atomic Habits",   "price": 399,   "category": "books",       "stock": 60, "rating": 4.9, "tags": ["self-help", "productivity", "education"]},
    "SKU012": {"name": "Python Crash Course", "price": 499, "category": "books",     "stock": 0,  "rating": 4.7, "tags": ["programming", "education", "beginner"]},
    "SKU013": {"name": "Olive Oil",       "price": 650,   "category": "food",        "stock": 35, "rating": 4.3, "tags": ["cooking", "healthy", "kitchen"]},
    "SKU014": {"name": "Green Tea",       "price": 299,   "category": "food",        "stock": 80, "rating": 4.5, "tags": ["beverage", "healthy", "organic"]},
    "SKU015": {"name": "Protein Powder",  "price": 1800,  "category": "food",        "stock": 18, "rating": 4.2, "tags": ["fitness", "healthy", "nutrition"]},
}

# ─────────────────────────────────────────
# 1. search_by_tag
# ─────────────────────────────────────────
def search_by_tag(tag):
    """
    Returns all products containing the given tag.
    Uses defaultdict to group results by tag.
    """
    tag_index = defaultdict(list)
    for sku, details in catalog.items():
        for t in details.get("tags", []):
            tag_index[t].append({"sku": sku, "name": details.get("name")})
    return tag_index.get(tag, [])

# ─────────────────────────────────────────
# 2. out_of_stock
# ─────────────────────────────────────────
def out_of_stock():
    """
    Returns products with stock == 0.
    Uses dict comprehension with filter.
    """
    return {
        sku: details.get("name")
        for sku, details in catalog.items()
        if details.get("stock", 0) == 0
    }

# ─────────────────────────────────────────
# 3. price_range
# ─────────────────────────────────────────
def price_range(min_price, max_price):
    """
    Returns products within the given price range.
    Uses .get() for safe access.
    """
    return {
        sku: details
        for sku, details in catalog.items()
        if min_price <= details.get("price", 0) <= max_price
    }

# ─────────────────────────────────────────
# 4. category_summary
# ─────────────────────────────────────────
def category_summary():
    """
    For each category: count, avg price, avg rating.
    Uses defaultdict(list) to collect values.
    """
    prices  = defaultdict(list)
    ratings = defaultdict(list)

    for details in catalog.values():
        cat = details.get("category", "unknown")
        prices[cat].append(details.get("price", 0))
        ratings[cat].append(details.get("rating", 0))

    return {
        cat: {
            "count":      len(prices[cat]),
            "avg_price":  round(sum(prices[cat])  / len(prices[cat]),  2),
            "avg_rating": round(sum(ratings[cat]) / len(ratings[cat]), 2),
        }
        for cat in prices
    }

# ─────────────────────────────────────────
# 5. apply_discount
# ─────────────────────────────────────────
def apply_discount(category, percent):
    """
    Reduces prices for all products in a category by given percent.
    Uses dict comprehension. Returns updated catalog.
    """
    return {
        sku: {
            **details,
            "price": round(details.get("price", 0) * (1 - percent / 100), 2)
        }
        if details.get("category") == category
        else (sku, details)
        for sku, details in catalog.items()
    }

# ─────────────────────────────────────────
# 6. merge_catalogs
# ─────────────────────────────────────────
def merge_catalogs(catalog1, catalog2):
    """
    Merges two catalogs using | operator.
    Duplicate SKUs: catalog2 values take priority.
    """
    return catalog1 | catalog2

# ─────────────────────────────────────────
# Main
# ─────────────────────────────────────────
if __name__ == "__main__":

    print("=" * 55)
    print("E-COMMERCE PRODUCT CATALOG SYSTEM")
    print("=" * 55)

    print("\n🔍 Search by tag 'portable':")
    for item in search_by_tag("portable"):
        print(f"   → {item['sku']}: {item['name']}")

    print("\nOut of Stock Products:")
    for sku, name in out_of_stock().items():
        print(f"   → {sku}: {name}")

    print("\nProducts between ₹500 and ₹5000:")
    for sku, d in price_range(500, 5000).items():
        print(f"   → {d.get('name')}: ₹{d.get('price')}")

    print("\nCategory Summary:")
    for cat, stats in category_summary().items():
        print(f"   {cat}: {stats}")

    print("\nApply 10% discount to 'electronics':")
    discounted = apply_discount("electronics", 10)
    for sku, d in discounted.items():
        if isinstance(d, dict) and d.get("category") == "electronics":
            print(f"   → {d.get('name')}: ₹{d.get('price')}")

    print("\nMerge Catalogs (catalog + extra):")
    extra_catalog = {
        "SKU016": {"name": "Coffee Maker", "price": 2499, "category": "home",
                   "stock": 10, "rating": 4.1, "tags": ["kitchen", "appliance"]},
    }
    merged = merge_catalogs(catalog, extra_catalog)
    print(f"   Total products after merge: {len(merged)}")
