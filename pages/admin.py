import streamlit as st
from utils.data_handling import save_products, load_offers, save_offers, save_selected_offer, load_selected_offer, get_current_offer
from utils.logs import parse_logs, aggregate_data

def admin_page():
    st.title("Admin Page")
    st.write("Welcome to the admin page!")
    st.sidebar.button('Exit Admin Page', on_click=lambda: st.session_state.update(page='command'))

    admin_option = st.sidebar.selectbox("Select Page", ["Stats", "Manage Products", "Manage Offers"])
    if admin_option == "Manage Products":
        st.subheader("Modify Product Prices")
        product_to_update = st.selectbox("Select Product", products)
        new_price = st.number_input("Enter new price", min_value=0.0, value=prices[products.index(product_to_update)])
        if st.button("Update Price"):
            prices[products.index(product_to_update)] = new_price
            save_products()
            st.success(f"Price updated for {product_to_update}")
    elif admin_option == "Manage Offers":
        st.subheader("Manage Offers")
        offers_df = load_offers()
        offer_options = ['None'] + [f"{row['offer_type']} - {row['x_value']} - {row['y_value']}" for index, row in offers_df.iterrows()] + ['Other']
        selected_offer = st.selectbox("Select an offer", offer_options, key='selected_offer')

        if selected_offer == 'Other':
            st.write("Create a new offer:")
            offer_type = st.selectbox("Offer Type", ['percentage', 'money'])
            x_value = st.number_input(f"Enter {'percentage' if offer_type == 'percentage' else 'amount'} value")
            y_value = st.number_input("Enter minimum total price or quantity")
            if st.button("Create Offer"):
                new_offer = pd.DataFrame({'offer_type': [offer_type], 'x_value': [x_value], 'y_value': [y_value]})
                offers_df = pd.concat([offers_df, new_offer], ignore_index=True)
                save_offers(offers_df)
                st.success("Offer created successfully")
        elif selected_offer != 'None':
            st.write(f"Selected Offer: {selected_offer}")
            save_selected_offer(selected_offer)
    elif admin_option == "Stats":
        show_stats()

def show_stats():
    st.subheader("Statistics")

    logs = parse_logs()
    orders_per_day, product_orders_df, stock_df = aggregate_data(logs)

    if orders_per_day is None:
        st.info("No transaction data to display.")
        return

    st.subheader("Orders per Product")
    st.bar_chart(product_orders_df.set_index('Product'))
