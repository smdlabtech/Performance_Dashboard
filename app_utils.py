import pandas as pd
import streamlit as st
import json



# Charger le thème depuis le fichier JSON
def load_theme():
    with open('assets/theme/theme.json') as f:
        return json.load(f)

theme = load_theme()


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