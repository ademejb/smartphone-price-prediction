# 03_visualisations.py
# Objectif : comprendre en images ce qui fait le prix
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("data/smartphones_clean.csv")

# Deux graphiques côte à côte
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# À gauche : le prix en euros
axes[0].hist(df["price_eur"], bins=40)
axes[0].set_title("Distribution du prix")
axes[0].set_xlabel("Prix (€)")
axes[0].set_ylabel("Nombre de téléphones")

# À droite : le logarithme du prix
axes[1].hist(np.log(df["price_eur"]), bins=40)
axes[1].set_title("Distribution du log du prix")
axes[1].set_xlabel("log(prix)")

plt.savefig("figures/01_distribution_prix.png", dpi=150, bbox_inches="tight")
plt.show()

# 2) Prix médian par marque, de la moins chère à la plus chère
prix_par_marque = df.groupby("brand_name")["price_eur"].median().sort_values()

fig, ax = plt.subplots(figsize=(8, 7))
ax.barh(prix_par_marque.index, prix_par_marque.values)
ax.set_title("Prix médian par marque")
ax.set_xlabel("Prix médian (€)")

plt.savefig("figures/02_prix_median_par_marque.png", dpi=150, bbox_inches="tight")
plt.show()

# 3) Prix selon le stockage et selon la RAM (boxplots)
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.boxplot(data=df, x="internal_memory", y="price_eur", ax=axes[0])
axes[0].set_title("Prix selon le stockage")
axes[0].set_xlabel("Stockage (Go)")
axes[0].set_ylabel("Prix (€)")

sns.boxplot(data=df, x="ram_capacity", y="price_eur", ax=axes[1])
axes[1].set_title("Prix selon la RAM")
axes[1].set_xlabel("RAM (Go)")
axes[1].set_ylabel("Prix (€)")

plt.savefig("figures/03_prix_stockage_ram.png", dpi=150, bbox_inches="tight")
plt.show()

# 4) Prix selon la 5G
fig, ax = plt.subplots(figsize=(6, 5))
sns.boxplot(data=df, x="5G_or_not", y="price_eur", ax=ax)
ax.set_title("Prix selon la 5G")
ax.set_xticks([0, 1])
ax.set_xticklabels(["Sans 5G", "Avec 5G"])
ax.set_xlabel("")
ax.set_ylabel("Prix (€)")

plt.savefig("figures/04_prix_5g.png", dpi=150, bbox_inches="tight")
plt.show()

# Les chiffres derrière le graphique
print(df.groupby("5G_or_not")["price_eur"].agg(["count", "median"]))

# 5) Carte des corrélations entre le prix et les caractéristiques techniques
colonnes = [
    "price_eur", "internal_memory", "ram_capacity", "processor_speed",
    "5G_or_not", "refresh_rate", "fast_charging", "screen_size",
    "primary_camera_rear", "battery_capacity",
]
correlations = df[colonnes].corr()

fig, ax = plt.subplots(figsize=(9, 7))
sns.heatmap(correlations, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, ax=ax)
ax.set_title("Corrélations entre les variables")

plt.savefig("figures/05_correlations.png", dpi=150, bbox_inches="tight")
plt.show()

# La colonne du prix, triée
print(correlations["price_eur"].sort_values(ascending=False))

# 6) Batterie selon le prix, en distinguant iPhone et Android
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(data=df, x="price_eur", y="battery_capacity", hue="os", alpha=0.6, ax=ax)
ax.set_title("Capacité de la batterie selon le prix")
ax.set_xlabel("Prix (€)")
ax.set_ylabel("Batterie (mAh)")

plt.savefig("figures/06_batterie_prix.png", dpi=150, bbox_inches="tight")
plt.show()