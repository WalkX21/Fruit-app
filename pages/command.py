import streamlit as st
from utils.data_handling import add_product, log_transaction, get_current_offer
from utils.pdf_receipt import create_receipt_pdf

def command_page():
    st.title('Command')

    st.sidebar.header('Product Selection')
    product_selection = products + ['Other']
    name = st.sidebar.selectbox('Which product', product_selection, key='name')

    if name == 'Other':
        with st.sidebar.expander('Create a new product'):
            st.text_input('Enter new product name', key='custom_product_name')
            st.number_input('Enter new product price per kg', min_value=0.00, value=0.0, key='custom_product_price')

    st.sidebar.header('Admin Access')
    password = st.sidebar.text_input('Enter password', type='password')
    
    if st.sidebar.button('Go'):
        if password == 'wewe':
            st.session_state.is_admin = True
            with open(LOG_FILE, 'rb') as file:
                st.sidebar.download_button('Download Log File', file, file_name='transaction_log.txt')

    if 'is_admin' in st.session_state and st.session_state.is_admin:
        st.sidebar.button('Admin Page', on_click=lambda: st.session_state.update(page='admin'))

    with st.form('Command'):
        st.header('Add a Product')

        col1, col2 = st.columns(2)
        with col1:
            how_many = st.number_input('How much (qt in kg)', min_value=0.00, max_value=10.00, value=0.0, key='how_many')
        with col2:
            date_input = st.date_input('Enter Date', value=date.today(), key='date')

            if name != 'Other':
                product_index = products.index(name)
                product_price = prices[product_index]
                st.write(f'Price per kg: {product_price} $')
            else:
                product_price = st.session_state.custom_product_price
                st.write(f'Price per kg: {product_price} $')

            if st.session_state.logged_in:
                users_df = pd.read_csv(USERS_FILE)
                user = users_df[users_df['username'] == st.session_state.username].iloc[0]
                if user['loyalty']:
                    st.write('**Loyalty Program Member**')
                    offer = get_current_offer()
                    if offer['offer_type'] == 'percentage':
                        st.write(f"**Offer: {offer['x_value']}% off on orders above {offer['y_value']} kg!**")
                    elif offer['offer_type'] == 'money':
                        st.write(f"**Offer: {offer['x_value']}$ off on orders above {offer['y_value']} $!**")
                    else:
                        st.write("**Offer: None yet**")
                else:
                    st.write("**Offer: None yet**")

        add_another = st.form_submit_button('Add Another Product', on_click=add_product)
        submit_button = st.form_submit_button('Submit Order')

    if st.session_state.order:
        st.subheader('Current Order')
        for i, product in enumerate(st.session_state.order):
            st.write(f"**Product {i + 1}:** {product['name']} - {product['quantity']} kg on {product['date']} with price of {product['price']} $/kg (Total: {round(product['quantity'] * product['price'], 2)} $)")

    if submit_button:
        st.subheader('Final Order')
        total_price = 0.0
        total_quantity = 0.0
        for i, product in enumerate(st.session_state.order):
            product_total = round(product['quantity'] * product['price'], 2)
            total_price += product_total
            total_quantity += product['quantity']
            st.write(f"**Product {i + 1}:** {product['name']} - {product['quantity']} kg on {product['date']} with price of {product['price']} $/kg (Total: {product_total} $)")

        users_df = pd.read_csv(USERS_FILE)
        user = users_df[users_df['username'] == st.session_state.username].iloc[0]
        discount = 0.0
        if user['loyalty']:
            offer = get_current_offer()
            if offer['offer_type'] == 'percentage' and total_quantity > offer['y_value']:
                discount = total_price * (offer['x_value'] / 100)
                st.write(f"**Discount ({offer['x_value']}% off):** -{round(discount, 2)} $")
            elif offer['offer_type'] == 'money' and total_price > offer['y_value']:
                discount = offer['x_value']
                st.write(f"**Discount ({offer['x_value']}$ off):** -{round(discount, 2)} $")
            total_price -= discount

        st.write(f"**Total Price:** {round(total_price, 2)} $")

        buffer = create_receipt_pdf(st.session_state.order, total_price, discount)
        st.download_button('Download Receipt PDF', buffer, file_name='receipt.pdf', mime='application/pdf')

        log_transaction(st.session_state.order, discount)
        st.session_state.order = []
