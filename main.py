import streamlit as st
from pages import login_signup, command, admin, stock_management, settings

if 'order' not in st.session_state:
    st.session_state.order = []

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'page' not in st.session_state:
    st.session_state.page = 'login'

def main():
    if not st.session_state.logged_in:
        if st.session_state.page == 'login':
            login_signup.login_page()
        elif st.session_state.page == 'signup':
            login_signup.signup_page()
    else:
        st.sidebar.header('Navigation')
        page = st.sidebar.radio('Go to', ['Command', 'Stock Management', 'Settings'])

        if st.session_state.page == 'admin':
            admin.admin_page()
        elif page == 'Command':
            st.session_state.page = 'command'
            command.command_page()
        elif page == 'Stock Management':
            st.session_state.page = 'stock_management'
            stock_management.stock_management_page()
        elif page == 'Settings':
            st.session_state.page = 'settings'
            settings.settings_page()

if __name__ == '__main__':
    main()

