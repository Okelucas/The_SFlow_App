import streamlit as st
import sqlite3
import pandas as pd
import json
from streamlit_lottie import st_lottie
import requests

def load_lottieur(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def logout_button():
    if st.sidebar.button("Deconnexion"):
        st.session_state.logged_in = False
        st.experimental_rerun()
        

# Fonction pour creer la table utilisateur dans la base de donnees
def create_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 username TEXT, 
                 password TEXT, 
                 age INTEGER, 
                 profession TEXT, 
                 nationalite TEXT,
                 interets_u TEXT)''')
    conn.commit()
    conn.close()




# Fonction pour inserer un nouveau sondage dans la base de donnees
def insert_user(username, password, age, profession, nationalite, interets_u):
    # Convertir la liste d'interets en une chaine de caracteres
    interets_str = ",".join(interets_u)
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''INSERT INTO users (username, password, age, profession, nationalite, interets_u) VALUES (?, ?, ?, ?, ?, ?)''',
              (username, password, age, profession, nationalite, interets_str))
    conn.commit()
    conn.close()

# Fonction pour recuperer les informations d'un utilisateur a partir de son nom d'utilisateur
def get_user_info(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM users WHERE username = ?''', (username,))
    user_info = c.fetchone()
    conn.close()

    # Convertir la chaine de caracteres d'interets en liste
    if user_info:
        user_info = list(user_info)
        user_info[6] = user_info[6].split(",") if user_info[6] else []  # Conversion de la chaine en liste
    return user_info

# Fonction pour verifier les informations de connexion
def authenticate(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM users WHERE username = ? AND password = ?''', (username, password))
    user_info = c.fetchone()
    conn.close()
    return user_info

# Fonction pour mettre a jour les informations de l'utilisateur
def update_user_info(id, password, age, profession, nationalite, interets_u):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Convert lists to strings
    profession_str = json.dumps(profession)
    nationalite_str = json.dumps(nationalite)
    interets_u_str = json.dumps(interets_u)

    c.execute('''UPDATE users SET password=?, age=?, profession=?, nationalite=?, interets_u=? WHERE id=?''', 
              (password, age, profession_str, nationalite_str, interets_u_str, id))
    conn.commit()
    conn.close()

# Function to retrieve surveys from the database
def retrieve_sondage():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM users''')
    users = c.fetchall()
    conn.close()

    # Convert strings back to lists
    for user in users:
        user['interets_sdg'] = json.loads(user['interets_sdg'])
        user['profession_cible'] = json.loads(user['profession_cible'])
        user['nationalite_cible'] = json.loads(user['nationalite_cible'])

    return users

# Creer la table utilisateur lors de la premiere execution de l'application
create_table()

# Page de connexion
def login_page():
    st.title("Connexion")
    lottie_login = load_lottieur("https://lottie.host/4693685d-6f24-4d30-bed3-01e0329aacb6/UEAgCxVyaU.json")
    st_lottie(lottie_login, key= "login" )
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        user_info = authenticate(username, password)
        if user_info:
            st.success("Connexion reussie!")
            lottie_login2 = load_lottieur("https://lottie.host/2ff5cf77-48eb-44f6-a69c-a4ddeed223a4/cF1cK7qz1U.json")
            st_lottie(lottie_login2, key= "login2")
            st.session_state.logged_in = True
            st.session_state.username = username
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")

# Page d'inscription
def signup_page():
    st.title("Inscription")
    prof_options = ['Eleve', 'Etudiant', 'Fonctionnaire', 'Sans Emploie']
    nat_opt = ["Francais", "Etranger"]
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    age = st.slider("Age", min_value=0, max_value=150)
    profession = st.selectbox("Quelle est votre profession ?", prof_options, index= None, placeholder= "Choisissez une option")
    nationalite = st.selectbox("Nationalite de l'utilisateur", nat_opt, index= None, placeholder= "Choisissez une option")
    centres_interets = ["Voyage", "Photographie", "Cuisine", "Randonnee", "Musique", 
                        "Lecture", "Art", "Sport", "Technologie", "Jardinage", 
                        "Cinema", "Jeux video", "Bricolage", "Danse", "Écriture", 
                        "Yoga", "Animaux", "Theatre", "Volontariat", "Mode"
                        ]
    interets_u = st.multiselect("Centres d'interets de l'utilisateur", centres_interets, placeholder= "Choisissez au moins trois options",)
    if st.button("S'inscrire"):
        insert_user(username, password, age, profession, nationalite, interets_u)
        if age is None or profession == "" or nationalite == "" or len(interets_u) == 0:
             st.error("Veuillez remplir tous les champs obligatoires.")
        if len(interets_u) < 3:
             st.error("Veuillez choisir au moins trois centres d'interet.")
        else:
            st.success("Inscription reussie! Vous pouvez maintenant vous connecter.")
            st.session_state.logged_in = True
            login_page()

# Page de profil

def profile_page():
    st.title("Profil")
    user_info = get_user_info(st.session_state.username)
    st.write(f"Nom d'utilisateur: {user_info[1]}")
    st.write(f"Age: {user_info[3]}")
    st.write(f"Profession: {user_info[4]}")
    st.write(f"Nationalite: {user_info[5]}")
    st.write(f"Centres d'interets: {user_info[6]}")

    st.subheader("Modifier les informations:")
    new_password = st.text_input("Nouveau mot de passe", value=user_info[2])
    new_age = st.number_input("Nouvel age", value=user_info[3], min_value=0, max_value=150)
    prof_options = ['Eleve', 'Etudiant', 'Fonctionnaire', 'Sans Emploie']
    new_profession = st.selectbox("Quelle est votre profession ?", prof_options)
    nat_opt = ["Francais", "Etranger"]
    new_nationalite = st.selectbox("Nationalite de l'utilisateur", nat_opt)
    centres_interets = ["Voyage", "Photographie", "Cuisine", "Randonnee", "Musique", 
                        "Lecture", "Art", "Sport", "Technologie", "Jardinage", 
                        "Cinema", "Jeux video", "Bricolage", "Danse", "Écriture", 
                        "Yoga", "Animaux", "Theatre", "Volontariat", "Mode"
                        ]
    new_interets_u = st.multiselect("Centres d'interets de l'utilisateur", centres_interets)
                                
    if st.button("Mettre a jour"):
        update_user_info(user_info[0], new_password, new_age, new_profession, new_nationalite, new_interets_u)
        st.success("Informations mises a jour avec succes!")


# Main function
def main():
    st.sidebar.header("Bienvenu sur")
    st.sidebar.image("S.png", width= 200)
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.session_state.username = ""
        menu = st.selectbox("", ("Inscription", "Connexion"))
        if menu == "Connexion":
            login_page()
        elif menu == "Inscription":
            signup_page()
    else:
        login_page()

if __name__ == "__main__":
    main()