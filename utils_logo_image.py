
import os

# 📂 Définition des dossiers
ROOT_DIR = os.getcwd()

# Chemin du logo
LOGO_PATH = os.path.join(ROOT_DIR, "assets", "img", "LOGO_AXYS_RVB.png")


# 🖼️ Charger et adapter dynamiquement le logo
if os.path.exists(LOGO_PATH):
    st.sidebar.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: auto;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    st.sidebar.image(LOGO_PATH, use_column_width=True)
else:
    st.sidebar.warning("⚠️ Logo non trouvé, vérifiez le chemin du fichier !")
