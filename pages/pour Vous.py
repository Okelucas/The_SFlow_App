import streamlit as st
import sqlite3
from sflow import *

try:
    if not st.session_state.logged_in:
        st.error("Vous n'êtes pas connecté(e) !")
        login_page()
    else:
        user_info = get_user_info(st.session_state.username)
        profession = user_info[4]
        nationalite = user_info[5]
        age = user_info[3]

        # Connexion à la base de données des sondages
        conn = sqlite3.connect('sondages.db')
        cursor = conn.cursor()

        # Requête SQL avec uniquement les colonnes nécessaires (titre_sdg et lien_sdg)
        query = """
        SELECT titre_sdg, lien_sdg
        FROM sondages
        WHERE profession_cible = ?
        OR nationalite_cible = ?
        OR ? BETWEEN age_min_cible AND age_max_cible
        """

        result = cursor.execute(query, (profession, nationalite, age)).fetchall()

        st.header("Résultats correspondant aux critères de l'utilisateur :")

        # Affichage de chaque sondage avec titre et lien séparés par une ligne markdown
        for row in result:
            titre_sdg, lien_sdg = row[0], row[1]
            #st.markdown(f"**{titre_sdg}**\n[{titre_sdg}]({lien_sdg})\n---")
            st.write(f"Titre du sondage : {titre_sdg}")
            st.write(f"URL : {lien_sdg}")
            #st.write(f"Creer par : {sondage[12]}")
            st.write("---------")
        # Fermeture de la connexion à la base de données des sondages
        conn.close()

except sqlite3.Error as e:
    st.error(f"Erreur SQLite : {e}")
except Exception as e:
    st.error(f"Une erreur s'est produite : {e}")
