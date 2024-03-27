import streamlit as st
from sflow import *

def logout_button():
    if st.button("Deconnexion"):
        st.session_state.logged_in = False
        st.experimental_rerun()


if not st.session_state.logged_in:
    st.error("Vous n'etes pas connecte(e) !")
    login_page()
else:
    profile_page()
    lottie_logout = load_lottieur("https://lottie.host/2ff5cf77-48eb-44f6-a69c-a4ddeed223a4/cF1cK7qz1U.json")
    st_lottie(lottie_logout, key= "logout", reverse=True )
    logout_button()