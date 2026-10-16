# 02_nettoyage.py
# Objectif : corriger les problèmes trouvés à l'exploration

import pandas as pd

df = pd.read_csv("data/smartphones.csv", encoding="utf-8-sig")

# Avant : combien de trous dans fast_charging ?
print("Trous avant :", df["fast_charging"].isna().sum())

# 1) Pas de charge rapide -> la puissance est 0 W
sans_charge_rapide = df["fast_charging_available"] == 0
df.loc[sans_charge_rapide, "fast_charging"] = 0

print("Trous après le 0 W :", df["fast_charging"].isna().sum())

# 2) Charge rapide de puissance inconnue -> médiane des téléphones AVEC charge rapide
avec_charge_rapide = df["fast_charging_available"] == 1
mediane_charge = df.loc[avec_charge_rapide, "fast_charging"].median()
print("Médiane de la charge rapide :", mediane_charge, "W")

df["fast_charging"] = df["fast_charging"].fillna(mediane_charge)

print("Trous restants :", df["fast_charging"].isna().sum())
# 3) avg_rating : 101 notes manquantes -> on supprime la colonne
#    (on ne peut pas inventer une note, et un nouveau téléphone n'en a pas encore)
df = df.drop(columns="avg_rating")
print("Taille après suppression :", df.shape)

# Où reste-t-il des trous ?
manquantes = df.isna().sum()
print(manquantes[manquantes > 0])
# 4) Colonnes de nombres : médiane
colonnes_nombres = ["num_cores", "processor_speed", "battery_capacity", "primary_camera_front"]
for col in colonnes_nombres:
    mediane = df[col].median()
    df[col] = df[col].fillna(mediane)
    print(col, "-> médiane :", mediane)

# 5) Colonnes de texte : valeur la plus fréquente (le mode)
colonnes_texte = ["processor_brand", "os"]
for col in colonnes_texte:
    plus_frequente = df[col].mode()[0]
    df[col] = df[col].fillna(plus_frequente)
    print(col, "-> valeur la plus fréquente :", plus_frequente)

# Vérification : nombre total de trous dans tout le tableau
print("Trous restants au total :", df.isna().sum().sum())
# 6) Les 12 téléphones les plus chers, avec leur RAM et leur stockage
colonnes_a_voir = ["brand_name", "model", "price", "ram_capacity", "internal_memory"]
plus_chers = df.sort_values("price", ascending=False)
print(plus_chers[colonnes_a_voir].head(12))
# 7) Retirer les téléphones de luxe : leur prix vient du luxe, pas des caractéristiques
telephones_luxe = [
    "Vertu Signature Touch",
    "Xiaomi Redmi K20 Pro Signature Edition",
    "Huawei Mate 50 RS Porsche Design",
    "Huawei Mate 30 RS Porsche Design",
]
a_retirer = df["model"].isin(telephones_luxe)
print("Téléphones retirés :", a_retirer.sum())

df = df[~a_retirer]
print("Taille après retrait :", df.shape)
print("Nouveau prix maximum :", df["price"].max())

# 8) Regrouper les marques de moins de 5 téléphones dans "autre"
comptes = df["brand_name"].value_counts()
petites_marques = comptes[comptes < 5].index

print("Marques regroupées :", len(petites_marques))
df.loc[df["brand_name"].isin(petites_marques), "brand_name"] = "autre"

print("Nombre de marques maintenant :", df["brand_name"].nunique())
print("Téléphones dans 'autre' :", (df["brand_name"] == "autre").sum())

# 9) Conversion en euros, avec un taux fixe proche de celui de 2023 (date des prix)
TAUX_INR_PAR_EUR = 90
df["price_eur"] = (df["price"] / TAUX_INR_PAR_EUR).round(0)

print(df[["model", "price", "price_eur"]].head())
print("Prix médian en euros :", df["price_eur"].median())
# 10) Enregistrer le tableau nettoyé
df.to_csv("data/smartphones_clean.csv", index=False)
print("Fichier enregistré :", df.shape)