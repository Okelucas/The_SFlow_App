import streamlit as st
import sqlite3
from sflow import *
import json

if not st.session_state.logged_in:
    st.error("Vous n'etes pas connecte(e) !")
    login_page()
# Fonction pour creer la table sondage dans la base de donnees
def create_table_s():
    conn = sqlite3.connect('sondages.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sondages
                 (id_s INTEGER PRIMARY KEY AUTOINCREMENT, 
                 titre_sdg TEXT, 
                 lien_sdg TEXT,
                 description_sdg TEXT, 
                 interets_sdg TEXT,
                 profession_cible TEXT,
                 nationalite_cible TEXT,
                 age_min_cible INTEGER,
                 age_max_cible INTEGER,
                 nbr_cible INTEGER,
                 nbr_q_sdg INTEGER,
                 duree_sdg INTEGER,
                 publisher TEXT,
                 credit_sdg INTEGER,
                 credit_cible INTEGER,
                 lien_credit TEXT)''')
    conn.commit()
    conn.close()


# Fonction pour inserer un nouvel utilisateur dans la base de donnees
    # Convertir la liste d'interets en une chaine de caracteres
    #interets_sdg_str = ",".join(interets_sdg)
    #profession_cible_str = ",".join(profession_cible)
    #nationalite_cible_str = ",".join(nationalite_cible)
def insert_sondage(titre_sdg, lien_sdg, description_sdg, interets_sdg, profession_cible, 
                   nationalite_cible, age_min_cible, age_max_cible, nbr_cible, nbr_q_sdg, 
                   duree_sdg, publisher, credit_sdg, credit_cible, lien_credit):
    conn = sqlite3.connect('sondages.db')
    c = conn.cursor()

    # Convert lists to strings
    interets_sdg_str = json.dumps(interets_sdg)
    profession_cible_str = json.dumps(profession_cible)
    nationalite_cible_str = json.dumps(nationalite_cible)

    c.execute('''INSERT INTO sondages (titre_sdg, lien_sdg, description_sdg, interets_sdg, profession_cible, 
                   nationalite_cible, age_min_cible, age_max_cible, nbr_cible, nbr_q_sdg, 
                   duree_sdg, publisher, credit_sdg, credit_cible, lien_credit) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (titre_sdg, lien_sdg, description_sdg, interets_sdg_str, profession_cible_str, 
               nationalite_cible_str, age_min_cible, age_max_cible, nbr_cible, nbr_q_sdg, 
               duree_sdg, publisher, credit_sdg, credit_cible, lien_credit))
    conn.commit()
    conn.close()

# Function to retrieve surveys from the database
def retrieve_sondage():
    conn = sqlite3.connect('sondages.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM sondages''')
    surveys = c.fetchall()
    conn.close()

    # Convert strings back to lists
    for survey in surveys:
        survey['interets_sdg'] = json.loads(survey['interets_sdg'])
        survey['profession_cible'] = json.loads(survey['profession_cible'])
        survey['nationalite_cible'] = json.loads(survey['nationalite_cible'])

    return surveys