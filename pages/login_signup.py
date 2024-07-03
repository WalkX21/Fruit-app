import streamlit as st
from utils.data_handling import authenticate, signup

def login_page():
    st.title('Welcome Back')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Login'):
            if authenticate(username, password):
                st.session_state.logged_in = True
                st.session_state.page = 'command'
                st.session_state.username = username
            else:
                st.error("Incorrect username or password")
    with col2:
        if st.button('Sign Up'):
            st.session_state.page = 'signup'

def signup_page():
    st.title('Sign Up')
    username = st.text_input('Username', key='signup_username')
    password = st.text_input('Password', type='password', key='signup_password')
    confirm_password = st.text_input('Confirm Password', type='password', key='confirm_password')
    loyalty = st.checkbox('Participate in Loyalty Program')
    phone = st.text_input('Phone Number') if loyalty else ''
    if password == confirm_password:
        if st.button('Register'):
            if signup(username, password, loyalty, phone):
                st.success("User registered successfully")
                st.session_state.page = 'login'
            else:
                st.error("Username already exists")
    else:
        st.error("Passwords do not match")
