import streamlit as st
from survey import *
from sflow import *

if not st.session_state.logged_in:
    st.error("Vous n'etes pas connecte(e) !")
    login_page()
else: 
    user_info = get_user_info(st.session_state.username)
    def create_sondage_page():

        st.title("Creer un nouveau sondage")

        titre_sdg = st.text_input("Titre du sondage")
        lien_sdg = st.text_input("Lien du sondage")
        description_sdg = st.text_area("Description du sondage")
        interets_sdg = st.multiselect("Interets du sondage", ["Voyage", "Photographie", 
                                                            "Cuisine", "Randonnee", "Musique", 
                                                            "Lecture", "Art", "Sport", "Technologie", "Jardinage", 
                                                            "Cinema", "Jeux video", "Bricolage", "Danse", "Écriture", 
                                                            "Yoga", "Animaux", "Theatre", "Volontariat", "Mode"
                                    ])
        profession_cible = st.multiselect("Profession cible", ['Eleve', 'Etudiant', 'Fonctionnaire', 'Sans Emploie'])
        nationalite_cible = st.multiselect("Nationalite cible", ["Francais", "Etranger"])
        age_min_cible = st.slider("Âge minimum cible", min_value=0, max_value=150)
        age_max_cible = st.slider("Âge maximum cible", min_value=0, max_value=150)
        nbr_cible = st.number_input("Nombre de personnes ciblees", min_value=0)
        nbr_q_sdg = st.number_input("Nombre de questions dans le sondage", min_value=0)
        duree_sdg = st.number_input("Duree du sondage (en minutes)", min_value=0)
        publisher = st.text_input("Éditeur du sondage", value=user_info[1])
        credit_sdg = st.number_input("Credit pour le sondage", min_value=0)
        credit_cible = st.number_input("Credit par reponse ciblee", min_value=0)
        lien_credit = st.text_input("Lien vers les credits du sondage")

        if st.button("Creer le sondage"):
            insert_sondage(titre_sdg, lien_sdg, description_sdg, interets_sdg, profession_cible, 
                nationalite_cible, age_min_cible, age_max_cible, nbr_cible, nbr_q_sdg, 
                duree_sdg, publisher, credit_sdg, credit_cible, lien_credit)
            create_table_s()
            st.success("Sondage cree avec succes!")

    # Fonction principale pour executer l'application

    
    create_sondage_page()
