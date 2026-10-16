# 01_exploration.py
# Objectif : découvrir le jeu de données avant de le nettoyer

import pandas as pd

# Afficher toutes les colonnes quand on imprime un tableau
pd.set_option("display.max_columns", None)

# Charger le fichier CSV dans un tableau Pandas
df = pd.read_csv("data/smartphones.csv", encoding="utf-8-sig")

# Taille du tableau : (nombre de lignes, nombre de colonnes)
print(df.shape)

# Les 5 premières lignes
print(df.head())
# Résumé : type de chaque colonne et nombre de valeurs non vides
df.info()
# Nombre de valeurs manquantes par colonne, de la plus touchée à la moins touchée
manquantes = df.isna().sum().sort_values(ascending=False)
print(manquantes[manquantes > 0])
# Statistiques sur le prix (en roupies indiennes)
print(df["price"].describe())

# Quelques quantiles en plus
print(df["price"].quantile([0.10, 0.90]))
# Nombre de marques différentes
print(df["brand_name"].nunique())

# Nombre de téléphones par marque (les 10 plus présentes)
print(df["brand_name"].value_counts().head(10))
# Marques avec moins de 5 téléphones
comptes = df["brand_name"].value_counts()
petites_marques = comptes[comptes < 5]

print("Nombre de petites marques :", len(petites_marques))
print("Nombre de téléphones concernés :", petites_marques.sum())
# Nombre de lignes en double (exactement identiques)
print("Doublons :", df.duplicated().sum())