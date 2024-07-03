


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