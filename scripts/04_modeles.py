# 04_modeles.py
# Objectif : prédire le prix d'un smartphone à partir de ses caractéristiques

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt

df = pd.read_csv("data/smartphones_clean.csv")

# y : la cible = le logarithme du prix en euros
y = np.log(df["price_eur"])

# X : les caractéristiques = toutes les colonnes sauf le nom et les prix
X = df.drop(columns=["model", "price", "price_eur"])

print("Taille de X :", X.shape)
print("Taille de y :", y.shape)
print(X.columns.tolist())

# Transformer les colonnes de texte en colonnes 0/1 (encodage one-hot)
X = pd.get_dummies(X, columns=["brand_name", "processor_brand", "os"], drop_first=True, dtype=int)

print("Taille de X après encodage :", X.shape)
print(X.columns.tolist())

# Séparer : 80 % pour apprendre, 20 % pour tester
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Entraînement :", X_train.shape)
print("Test :", X_test.shape)

# Modèle 1 : régression linéaire
lineaire = LinearRegression()
lineaire.fit(X_train, y_train)

# Prédictions sur le test (en log), puis retour en euros avec exp
pred_log_lin = lineaire.predict(X_test)
prix_predits_lin = np.exp(pred_log_lin)
prix_reels = np.exp(y_test)

# Évaluation
mae_lin = mean_absolute_error(prix_reels, prix_predits_lin)
r2_lin = r2_score(y_test, pred_log_lin)
print("Régression linéaire : MAE =", round(mae_lin), "€ | R² =", round(r2_lin, 3))

# Modèle 2 : forêt aléatoire (300 arbres)
foret = RandomForestRegressor(n_estimators=300, random_state=42)
foret.fit(X_train, y_train)

pred_log_foret = foret.predict(X_test)
prix_predits_foret = np.exp(pred_log_foret)

mae_foret = mean_absolute_error(prix_reels, prix_predits_foret)
r2_foret = r2_score(y_test, pred_log_foret)
print("Forêt aléatoire : MAE =", round(mae_foret), "€ | R² =", round(r2_foret, 3))

# Erreur relative : écart en % du prix réel, pour chaque téléphone du test
erreurs_pct_lin = np.abs(prix_predits_lin - prix_reels) / prix_reels * 100
erreurs_pct_foret = np.abs(prix_predits_foret - prix_reels) / prix_reels * 100

print("Erreur médiane, régression :", round(np.median(erreurs_pct_lin), 1), "%")
print("Erreur médiane, forêt :", round(np.median(erreurs_pct_foret), 1), "%")

# Graphique : prix prédit vs prix réel (forêt aléatoire)
fig, ax = plt.subplots(figsize=(6, 6))
ax.scatter(prix_reels, prix_predits_foret, alpha=0.6)

# La diagonale : là où prédit = réel
limite = max(prix_reels.max(), prix_predits_foret.max())
ax.plot([0, limite], [0, limite], color="red", linestyle="--", label="Prédiction parfaite")

# Échelles logarithmiques
ax.set_xscale("log")
ax.set_yscale("log")

ax.set_title("Forêt aléatoire : prix prédit vs prix réel")
ax.set_xlabel("Prix réel (€)")
ax.set_ylabel("Prix prédit (€)")
ax.legend()

plt.savefig("figures/07_predit_vs_reel.png", dpi=150, bbox_inches="tight")
plt.show()

# Importance des variables pour la forêt aléatoire (les 15 premières)
importances = pd.Series(foret.feature_importances_, index=X.columns)
top15 = importances.sort_values().tail(15)

fig, ax = plt.subplots(figsize=(8, 6))
ax.barh(top15.index, top15.values)
ax.set_title("Forêt aléatoire : importance des variables")
ax.set_xlabel("Importance")

plt.savefig("figures/08_importance_variables.png", dpi=150, bbox_inches="tight")
plt.show()

print(importances.sort_values(ascending=False).head(10))