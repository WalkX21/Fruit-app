import pandas as pd
import os
from datetime import datetime

LOG_FILE = 'transaction_log.txt'

def parse_logs():
    if not os.path.exists(LOG_FILE):
        return [], []

    logs = []
    with open(LOG_FILE, 'r') as f:
        lines = f.readlines()
        transaction = {}
        for line in lines:
            if line.startswith("Transaction at"):
                if transaction:
                    logs.append(transaction)
                transaction = {'timestamp': line.split("Transaction at")[1].strip(), 'products': []}
            elif "kg on" in line:
                parts = line.split("kg on")
                product_part = parts[0].strip()
                product_name, quantity = product_part.split(" - ")
                quantity = float(quantity.split(" ")[0])
                price_part = parts[1].split("with price of")[1].strip()
                price = float(price_part.split(" $/kg")[0])
                total_price = float(price_part.split(" (Total: ")[1].replace(" $)", ""))
                transaction['products'].append({
                    'name': product_name,
                    'quantity': quantity,
                    'price': price,
                    'total': total_price
                })
            elif "Discount applied:" in line:
                discount = float(line.split("Discount applied: -")[1].strip().replace(" $", ""))
                transaction['discount'] = discount
        if transaction:
            logs.append(transaction)

    return logs

def aggregate_data(logs):
    if not logs:
        return None, None, None

    transactions_df = pd.DataFrame(logs)
    transactions_df['timestamp'] = pd.to_datetime(transactions_df['timestamp'])

    orders_per_day = transactions_df['timestamp'].dt.date.value_counts().sort_index()

    product_orders = {}
    for transaction in logs:
        if 'products' in transaction:
            for product in transaction['products']:
                if product['name'] not in product_orders:
                    product_orders[product['name']] = 0
                product_orders[product['name']] += product['quantity']

    product_orders_df = pd.DataFrame(list(product_orders.items()), columns=['Product', 'Quantity'])

    return orders_per_day, product_orders_df, stock_df
