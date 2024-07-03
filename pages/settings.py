import streamlit as st
from utils.data_handling import USERS_FILE
import pandas as pd

def settings_page():
    st.title('Settings')
    users_df = pd.read_csv(USERS_FILE)
    user = users_df[users_df['username'] == st.session_state.username].iloc[0]

    st.subheader('Profile Information')
    new_username = st.text_input('Username', user['username'])
    loyalty = st.checkbox('Participate in Loyalty Program', user['loyalty'])
    phone = st.text_input('Phone Number', user['phone']) if loyalty else ''

    if st.button('Update Profile'):
        users_df.loc[users_df['username'] == user['username'], 'username'] = new_username
        users_df.loc[users_df['username'] == user['username'], 'loyalty'] = loyalty
        if loyalty:
            users_df.loc[users_df['username'] == user['username'], 'phone'] = phone
        users_df.to_csv(USERS_FILE, index=False)
        st.success("Profile updated successfully")
