import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import json

# Configuration de la page
st.set_page_config(
    page_title="Comprehensive KPI Dashboard",
    page_icon="📊",
    layout="wide",
)

# Charger le thème depuis le fichier JSON
def load_theme():
    with open('assets/theme/theme.json') as f:
        return json.load(f)

theme = load_theme()

# Charger les données depuis le fichier CSV
@st.cache_data
def load_data():
    file_path = "_data/simulated_streamlit_data.csv"  # Chemin du fichier CSV généré
    return pd.read_csv(file_path)

data = load_data()

# Ajouter des colonnes fictives pour les nouveaux KPIs
data["Transactions"] = np.random.randint(50, 500, size=len(data))
data["Customer Satisfaction"] = np.random.uniform(70, 100, size=len(data)).round(2)
data["Cost per Acquisition"] = np.random.uniform(10, 50, size=len(data)).round(2)

# Fonction pour créer un conteneur KPI avec valeur, étiquette et style CSS.
def containerize_kpi(kpi_value, kpi_label, change=None):
    """
    Cette fonction crée un conteneur KPI avec une valeur et une étiquette.
    Elle prend trois paramètres : kpi_value, kpi_label et change.
    Elle retourne une chaîne contenant le code HTML pour le conteneur KPI.
    """
    arrow = ""
    color = theme['foreground']  # Couleur par défaut

    if change is not None:
        if change > 0:
            arrow = "▲"  # Flèche vers le haut
            color = "green"
        elif change < 0:
            arrow = "▼"  # Flèche vers le bas
            color = "red"

    return f"""
    <style>
        .kpi-container {{
            width: 250px;  /* Largeur augmentée */
            height: 100px; /* Hauteur fixe */
            border: 1px solid {theme['foregroundNeutralSecondary']};
            border-radius: 8px;
            padding: 16px;
            text-align: center;
            background-color: {theme['backgroundLight']};
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}
        .kpi-value {{
            font-size: 24px;
            font-weight: bold;
            color: {color};
        }}
        .kpi-label {{
            font-size: 14px;
            color: {theme['foregroundNeutralTertiary']};
        }}
        .kpi-change {{
            font-size: 14px;
            color: {color};
        }}
    </style>
    <div class="kpi-container">
        <div class="kpi-value">{kpi_value} {arrow}</div>
        <div class="kpi-label">{kpi_label}</div>
        {f'<div class="kpi-change">{change:+.2f}</div>' if change is not None else ''}
    </div>
    """

# Sidebar pour la navigation
st.sidebar.title("Navigation")
st.sidebar.write("Sélectionnez une page ci-dessous :")

# Onglets pour la navigation
tab1, tab2, tab3 = st.tabs(["Dashboard", "Insights", "Data"])


#-----------------#
# Page : Dashboard
#-----------------#
with tab1:
    st.title("Performance Dashboard")
    # st.subheader("A complete overview of all performance metrics")

    # Affichage des KPIs en haut de la page
    st.write("### Key Performance Indicators")
    col1, col2, col3, col4, col5 = st.columns(5)

    # Calcul des KPIs
    total_visitors = data["Visitors"].sum()
    total_revenue = data["Revenue"].sum()
    total_transactions = data["Transactions"].sum()
    average_revenue_per_transaction = total_revenue / total_transactions if total_transactions > 0 else 0
    global_conversion_rate = (total_transactions / total_visitors) * 100 if total_visitors > 0 else 0

    # Simuler des variations pour l'exemple
    previous_total_visitors = total_visitors - np.random.randint(100, 500)
    previous_total_revenue = total_revenue - np.random.randint(1000, 5000)
    previous_total_transactions = total_transactions - np.random.randint(10, 50)

    with col1:
        st.markdown(containerize_kpi(f"{total_visitors:,}", "Total Visitors", total_visitors - previous_total_visitors), unsafe_allow_html=True)

    with col2:
        st.markdown(containerize_kpi(f"${total_revenue:,.2f}", "Total Revenue", total_revenue - previous_total_revenue), unsafe_allow_html=True)

    with col3:
        st.markdown(containerize_kpi(f"{global_conversion_rate:.2f}%", "Global Conversion Rate"), unsafe_allow_html=True)

    with col4:
        st.markdown(containerize_kpi(f"{total_transactions:,}", "Total Transactions", total_transactions - previous_total_transactions), unsafe_allow_html=True)

    with col5:
        st.markdown(containerize_kpi(f"${average_revenue_per_transaction:,.2f}", "Revenue per Transaction"), unsafe_allow_html=True)

    # Filtres sur la page
    st.write("### Filters")
    col1, col2 = st.columns([1, 1])  # Colonnes de largeur égale

    with col1:
        start_date = st.date_input("Start Date", value=pd.to_datetime(data["Date"]).min())

    with col2:
        end_date = st.date_input("End Date", value=pd.to_datetime(data["Date"]).max())

    selected_channels = st.multiselect(
        "Select Channels", options=data["Channel"].unique(), default=data["Channel"].unique()
    )
    selected_categories = st.multiselect(
        "Select Categories", options=data["Category"].unique(), default=data["Category"].unique()
    )

    # Application des filtres
    filtered_data = data[
        (pd.to_datetime(data["Date"]) >= pd.to_datetime(start_date)) &
        (pd.to_datetime(data["Date"]) <= pd.to_datetime(end_date)) &
        (data["Channel"].isin(selected_channels)) &
        (data["Category"].isin(selected_categories))
    ]

    # Graphiques
    st.write("### Performance Insights")
    col1, col2 = st.columns(2)

    with col1:
        # Graphique d'évolution des visiteurs et des revenus
        fig1 = px.line(
            filtered_data.groupby("Date").sum().reset_index(),
            x="Date", y=["Visitors", "Revenue"],
            title="Visitors and Revenue Over Time",
            labels={"value": "Metric Value", "variable": "Metrics"}
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        # Graphique à barres : Répartition des revenus par catégorie
        average_revenue_per_category = filtered_data.groupby("Category")["Revenue"].mean()
        fig2 = px.bar(
            average_revenue_per_category.reset_index(),
            x="Category", y="Revenue", color="Category",
            title="Average Revenue per Category",
            labels={"Revenue": "Avg Revenue"}
        )
        st.plotly_chart(fig2, use_container_width=True)

#-----------------#
# Page : Insights
#-----------------#
with tab2:
    st.title("Detailed Insights")

    # Sunburst Chart : Répartition des revenus par catégorie et canal
    fig3 = px.sunburst(
        filtered_data,
        path=["Channel", "Category"],
        values="Revenue",
        title="Revenue Breakdown by Channel and Category",
        color="Revenue",
    )
    st.plotly_chart(fig3, use_container_width=True)

#-------------#
# Page : Data
#------------#
with tab3:
    st.title("Data")
    st.dataframe(data)

    # Téléchargement des données filtrées
    # st.write("### Download Data")
    csv = data.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="filtered_data.csv",
        mime="text/csv"
    )