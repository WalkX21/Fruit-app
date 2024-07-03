import pandas as pd
import os

PRODUCTS_FILE = 'products.csv'
LOG_FILE = 'transaction_log.txt'
STOCK_FILE = 'stock.csv'
USERS_FILE = 'users.csv'
OFFERS_FILE = 'offers.csv'
SELECTED_OFFER_FILE = 'selected_offer.txt'

# Load product data from CSV
if os.path.exists(PRODUCTS_FILE):
    products_df = pd.read_csv(PRODUCTS_FILE)
    products = products_df['product'].tolist()
    prices = products_df['price'].tolist()
else:
    products = ['Tomatoes 🍅', 'Potatoes 🥔', 'Carrots 🥕', 'Cucumber 🥒', 'Lettuce 🥬']
    prices = [1.5, 1.0, 0.8, 1.2, 0.9]
    products_df = pd.DataFrame({'product': products, 'price': prices})
    products_df.to_csv(PRODUCTS_FILE, index=False)

if os.path.exists(STOCK_FILE):
    stock_df = pd.read_csv(STOCK_FILE)
else:
    stock_df = pd.DataFrame({'product': products, 'stock': [100] * len(products)})
    stock_df.to_csv(STOCK_FILE, index=False)

if not os.path.exists(USERS_FILE):
    users_df = pd.DataFrame(columns=['username', 'password', 'loyalty', 'phone'])
    users_df.to_csv(USERS_FILE, index=False)

if not os.path.exists(OFFERS_FILE):
    offers_df = pd.DataFrame(columns=['offer_type', 'x_value', 'y_value'])
    offers_df.to_csv(OFFERS_FILE, index=False)

if not os.path.exists(SELECTED_OFFER_FILE):
    with open(SELECTED_OFFER_FILE, 'w') as f:
        f.write("None")

def save_products():
    df = pd.DataFrame({'product': products, 'price': prices})
    df.to_csv(PRODUCTS_FILE, index=False)

def save_stock():
    stock_df.to_csv(STOCK_FILE, index=False)

def save_offers(offers_df):
    offers_df.to_csv(OFFERS_FILE, index=False)

def load_offers():
    if os.path.exists(OFFERS_FILE):
        return pd.read_csv(OFFERS_FILE)
    return pd.DataFrame(columns=['offer_type', 'x_value', 'y_value'])

def save_selected_offer(selected_offer):
    with open(SELECTED_OFFER_FILE, 'w') as f:
        f.write(selected_offer)

def load_selected_offer():
    if os.path.exists(SELECTED_OFFER_FILE):
        with open(SELECTED_OFFER_FILE, 'r') as f:
            return f.read().strip()
    return "None"

def authenticate(username, password):
    users_df = pd.read_csv(USERS_FILE)
    user = users_df[(users_df['username'] == username) & (users_df['password'] == password)]
    return not user.empty

def signup(username, password, loyalty, phone):
    users_df = pd.read_csv(USERS_FILE)
    if username in users_df['username'].values:
        return False
    new_user = pd.DataFrame({'username': [username], 'password': [password], 'loyalty': [loyalty], 'phone': [phone]})
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    users_df.to_csv(USERS_FILE, index=False)
    return True

def add_product():
    if st.session_state.name == 'Other':
        product_name = st.session_state.custom_product_name
        product_price = st.session_state.custom_product_price
        if product_name not in products:
            products.append(product_name)
            prices.append(product_price)
            save_products()
            stock_df.loc[len(stock_df)] = [product_name, 100]
            save_stock()
    else:
        product_name = st.session_state.name
        product_index = products.index(product_name)
        product_price = prices[product_index]

    product = {
        'name': product_name,
        'quantity': st.session_state.how_many,
        'date': st.session_state.date,
        'price': product_price
    }
    stock_index = stock_df[stock_df['product'] == product_name].index[0]
    if product['quantity'] > stock_df.at[stock_index, 'stock']:
        st.error(f"Not enough stock for {product_name}")
    else:
        stock_df.at[stock_index, 'stock'] -= product['quantity']
        st.session_state.order.append(product)
        save_stock()

def log_transaction(order, discount):
    with open(LOG_FILE, 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"Transaction at {timestamp}\n")
        for product in order:
            f.write(f"{product['name']} - {product['quantity']} kg on {product['date']} with price of {product['price']} $/kg (Total: {product['quantity'] * product['price']} $)\n")
        if discount > 0:
            f.write(f"Discount applied: -{discount:.2f} $\n")
        f.write("\n")

def get_current_offer():
    selected_offer_str = load_selected_offer()
    if selected_offer_str == "None":
        return {'offer_type': 'none', 'x_value': 0, 'y_value': 0}
    offer_parts = selected_offer_str.split(" - ")
    offer_type = offer_parts[0]
    x_value = float(offer_parts[1])
    y_value = float(offer_parts[2])
    return {'offer_type': offer_type, 'x_value': x_value, 'y_value': y_value}
