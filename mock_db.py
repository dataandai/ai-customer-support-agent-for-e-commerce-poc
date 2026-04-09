from typing import Dict, List, Optional

ORDERS = {
    "ORD-101": {"status": "Shipped", "delivery_date": "2023-10-25", "items": ["Wireless Mouse", "Keyboard"]},
    "ORD-102": {"status": "Processing", "delivery_date": "TBD", "items": ["Gaming Monitor"]},
    "ORD-103": {"status": "Delivered", "delivery_date": "2023-10-20", "items": ["USB-C Cable"]}
}

PRODUCTS = [
    {"id": 1, "name": "Wireless Mouse", "price": 25.99, "stock": 50},
    {"id": 2, "name": "Keyboard", "price": 45.00, "stock": 12},
    {"id": 3, "name": "Gaming Monitor", "price": 299.99, "stock": 5}
]

REFUND_POLICY = """
Customers can return items within 30 days of purchase. 
Items must be in original packaging. 
Refunds take 5-7 business days to process once the item is received.
Electronics have a 15% restocking fee if opened.
"""

def get_order(order_id: str) -> Optional[Dict]:
    return ORDERS.get(order_id)

def search_products(query: str) -> List[Dict]:
    return [p for p in PRODUCTS if query.lower() in p['name'].lower()]

def get_refund_policy() -> str:
    return REFUND_POLICY