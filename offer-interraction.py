



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

def get_current_offer():
    selected_offer_str = load_selected_offer()
    if selected_offer_str == "None":
        return {'offer_type': 'none', 'x_value': 0, 'y_value': 0}
    offer_parts = selected_offer_str.split(" - ")
    offer_type = offer_parts[0]
    x_value = float(offer_parts[1])
    y_value = float(offer_parts[2])
    return {'offer_type': offer_type, 'x_value': x_value, 'y_value': y_value}