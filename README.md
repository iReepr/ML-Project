# FTML 2025 Project

## Description générale

Ce projet de Machine Learning comprend plusieurs exercices indépendants, combinant des aspects mathématiques (taggés *M*) et de programmation en Python (taggés *C*). L’objectif est d’appliquer et approfondir les concepts étudiés en cours, en travaillant sur des problèmes variés allant de l’estimation bayésienne à la prédiction et au clustering.

Chaque exercice est organisé dans son propre dossier avec un notebook Python et/ou un rapport expliquant la démarche, les choix méthodologiques et les résultats.

---

## Liste des exercices

| Exercice | Type | Description                                                                                |
| -------- | ---- | ------------------------------------------------------------------------------------------ |
| 1        | M    | Estimation bayésienne et risque bayésien sur un problème supervisé personnalisé            |
| 2        | C    | Simulation d’un estimateur et comparaison avec l’estimateur bayésien                       |
| 3        | M    | Valeur attendue du risque empirique pour la régression OLS                                 |
| 4        | C    | Régression supervisée sur un dataset donné                                                 |
| 5        | C    | Classification supervisée sur un dataset donné                                             |
| 6        | C    | **Prédiction de la valeur marchande des joueurs de football (régression supervisée)**      |
| 7        | C    | **Clustering des équipes selon leur style de jeu (clustering non supervisé et supervisé)** |

---

## Détail des exercices clés

## Données utilisées

Le dataset utilisé dans ce projet a été scrapé.

* Les statistiques détaillées des joueurs proviennent des 5 grands championnats européens (Premier League, La Liga, Serie A, Bundesliga, Ligue 1) pour la saison 2024/2025, issues du dataset initial disponible sur [Kaggle](https://www.kaggle.com/datasets/hubertsidorowicz/football-players-stats-2024-2025).
* Les valeurs marchandes des joueurs ont été récupérées depuis le site [Transfermarkt](https://www.transfermarkt.com/). Le notebook `add_market_value.ipynb` dans le dossier `scrap` montre comment ces données ont été intégrées au dataset.
* Les informations sur les fins de contrat des joueurs proviennent du site [sofifa.com](https://www.sofifa.com/). Le code associé est disponible dans le repo [sofifa-web-scraper](https://github.com/SolideSpoke/sofifa-web-scraper/tree/main).

L’ensemble des scripts utilisés pour collecter, nettoyer et fusionner ces données se trouve dans le dossier `scrap` du projet.

Vous pouvez retrouver la description complète des features utilisées dans le fichier [features.md](features.md) fourni dans le projet.


### Exercice 6 – Prédiction de la valeur marchande

* **Objectif** : prédire la valeur marchande (`market_value`) des joueurs de football professionnels à partir de leurs caractéristiques et performances.
* **Dataset** : statistiques détaillées de 1887 joueurs issus des 5 grands championnats européens (saison 2024/2025).
* **Méthodologie** :

  * Prétraitement et sélection des features.
  * Application de modèles de régression supervisée (régressions linéaires, arbres, etc.).
  * Évaluation et comparaison des performances.

### Exercice 7 – Clustering des équipes par style de jeu

* **Objectif** : regrouper les équipes en fonction de leur style de jeu via leurs statistiques agrégées.
* **Approche** :

  * Clustering non supervisé avec Mean Shift (nombre de clusters non fixé).
  * Évaluation des clusters via indices de silhouette, Davies-Bouldin et Calinski-Harabasz.
  * Clustering supervisé avec KMeans fixé à 5 clusters (nombre de championnats).
  * Comparaison avec la classification réelle via l’Adjusted Rand Index (ARI).

---

