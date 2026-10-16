# 05_export_powerbi.py
# Objectif : préparer le fichier lu par le tableau de bord Power BI

import pandas as pd

df = pd.read_csv("data/smartphones_clean.csv")

# Prix en nombre entier : Power BI en français attend une virgule décimale
# et lirait "433.0" comme du texte
df["price_eur"] = df["price_eur"].astype(int)

# Gamme de prix : entrée < 200 €, milieu 200-500 €, haut > 500 €
def gamme(prix):
    if prix < 200:
        return "Entrée de gamme"
    elif prix <= 500:
        return "Milieu de gamme"
    else:
        return "Haut de gamme"

df["gamme"] = df["price_eur"].apply(gamme)

# 5G en "Oui" / "Non" pour que le filtre soit lisible
df["5G"] = df["5G_or_not"].map({0: "Non", 1: "Oui"})

# Seulement les colonnes utiles au tableau de bord
colonnes = [
    "brand_name", "model", "price_eur", "gamme", "5G", "os",
    "ram_capacity", "internal_memory", "processor_brand", "processor_speed",
    "battery_capacity", "screen_size", "refresh_rate",
]
df[colonnes].to_csv("data/smartphones_powerbi.csv", index=False)

print(df["gamme"].value_counts())
print("Fichier Power BI enregistré :", df[colonnes].shape)