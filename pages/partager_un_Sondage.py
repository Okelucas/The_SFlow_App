import streamlit as st
from sflow import *
from survey import *


if not st.session_state.logged_in:
    st.error("Vous n'etes pas connecte(e) !")
    login_page()

else:
    user_info = get_user_info(st.session_state.username)
    # Fonction pour recuperer les sondages publies par l'utilisateur connecte
    def get_user_sondages(username):
        conn = sqlite3.connect('sondages.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM sondages WHERE publisher = ?''', (username,))
        sondages = c.fetchall()
        conn.close()
        return sondages

    # Fonction pour afficher les sondages publies par l'utilisateur connecte
    def display_user_sondages(username):
        st.title("Mes Sondages")

        sondages = get_user_sondages(username)
        
        if not sondages:
            st.write("Vous n'avez publie aucun sondage pour le moment.")
        else:
            for sondage in sondages:
                st.write(f"Titre du sondage : {sondage[1]}")
                st.write(f"URL : {sondage[2]}")
                st.write(f"Creer par : {sondage[12]}")
                st.write("---------")
    get_user_info(username = user_info[1])
    display_user_sondages(username = user_info[1])