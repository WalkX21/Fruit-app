import streamlit as st
from utils.data_handling import save_stock, stock_df, products

def stock_management_page():
    st.title('Stock Management')

    st.subheader('Stock Database')
    st.table(stock_df)

    with st.form('Update Stock'):
        product = st.selectbox('Select Product', products)
        new_stock = st.number_input('Enter new stock quantity', min_value=0)
        update_button = st.form_submit_button('Update Stock')

    if update_button:
        stock_index = stock_df[stock_df['product'] == product].index[0]
        stock_df.at[stock_index, 'stock'] = new_stock
        save_stock()
        st.success(f"Stock updated for {product}")
