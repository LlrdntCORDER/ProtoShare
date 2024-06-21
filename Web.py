import streamlit as st
import pandas as pd

# Charger le fichier Excel
@st.cache_data
def load_data(file_path):
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, 'CADASTRE')
    return df

# Afficher chaque entrée sous la forme d'un cadre 
def display_entries(df, titre_filter):
    num_columns = 3
    filtered_df = df[df['Titre'].str.contains(titre_filter, case=False, na=False)] if titre_filter else df
    for i in range(0, len(filtered_df), num_columns):
        row = filtered_df.iloc[i:i+num_columns]
        columns = st.columns(num_columns)
        for col, (index, row_data) in zip(columns, row.iterrows()):
            with col:
                if st.button(str(row_data['Titre']), key=f"button_{index}"):
                    st.session_state['selected_row'] = row_data

def show_details(row_data):
    st.markdown(f"""
    <div style="background-color: #f0f0f0; padding: 20px; border-radius: 15px; width: 100%;">
        <h2>{row_data['Titre']}</h2>
        <p><strong>Organisme:</strong> {row_data['Organisme']}</p>
        <p><strong>Date de publication:</strong> {row_data['Date de publication']}</p>
        <p><strong>Objectifs:</strong> {row_data['Objectifs']}</p>
        <p><strong>Mots clés:</strong> {row_data['Mots clés']}</p>
        <p><strong>Lien d'accès:</strong> <a href='{row_data["Lien d'accès"]}'>Accéder</a></p>
        <p><strong>Collaborateurs:</strong> {row_data['Collaborateurs']}</p>
    </div>
""", unsafe_allow_html=True)


# Interface Streamlit
st.title('Cadastre')

# Charger les données
file_path = 'https://github.com/LlrdntCORDER/ProtoShare/blob/main/20220425_CADASTRESEM.xlsx'
df = load_data(file_path)

# Barre de recherche pour le titre sans autocomplétion
titre_filter = st.text_input('Rechercher par Titre', '')

# Menu de filtres
st.sidebar.title("Filtres")

# Filtre par Axe de recherche
axes_recherche = df['Axe de recherche'].dropna().unique()
selected_axes = st.sidebar.multiselect('Axe de recherche', axes_recherche)

# Filtre par Thèmes
themes = df['Thèmes'].dropna().unique()
selected_themes = st.sidebar.multiselect('Thèmes', themes)

# Filtre par Types d'expertise
types_expertise = df["Types d'expertise"].dropna().unique()
selected_types = st.sidebar.multiselect('Types d\'expertise', types_expertise)

# Barre de recherche pour Référant sans autocomplétion
referant_filter = st.sidebar.text_input('Référant', '')

# Appliquer les filtres
if selected_axes:
    df = df[df['Axe de recherche'].isin(selected_axes)]
if selected_themes:
    df = df[df['Thèmes'].isin(selected_themes)]
if selected_types:
    df = df[df["Types d'expertise"].isin(selected_types)]
if referant_filter:
    df = df[df['Référant'].str.contains(referant_filter, case=False, na=False)]
if titre_filter:
    df = df[df['Titre'].str.contains(titre_filter, case=False, na=False)]

# Définition du style CSS
custom_css = """
<style>
.st-emotion-cache-13ln4jf{
max-width:90%;
}
.st-emotion-cache-j6qv4b{
    text-align: left;
    justify-content: left;
}
body {
    font-family: Arial, sans-serif;
    background-color: #f8f9fa;
}
h2 {
    color: #0069d9;
    font-size: 150%;
}
</style>
"""

# Injecter le style CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Diviser la page en deux colonnes avec plus de place pour la grille de cadre
col1, col2 = st.columns([4, 3])

with col1:
    display_entries(df, titre_filter)

with col2:
    if 'selected_row' in st.session_state:
        show_details(st.session_state['selected_row'])
    else:
        st.write("Sélectionnez une case pour afficher les détails ici.")
