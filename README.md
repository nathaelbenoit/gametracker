# GameTracker - Pipeline ETL

## Description

**GameTracker** est une application Python qui implémente un pipeline ETL (Extract, Transform, Load) pour traiter et analyser les données de joueurs et de scores vidéo. Le projet démontre les bonnes pratiques d'automatisation, de qualité des données et de gestion d'une base de données.

## Prérequis techniques

- **Docker** et **Docker Compose** (version 3.9+)
- **Python** 3.11
- **MySQL** 8.0
- Les packages Python listés dans `requirements.txt` :
  - `mysql-connector-python`
  - `pandas`

## Instructions de lancement

### 1. Démarrer les services Docker

```bash
docker compose up -d
```

Cette commande démarre deux services :
- **db** : MySQL 8.0 avec healthcheck
- **app** : Application Python

### 2. Exécuter le pipeline complet

```bash
docker compose run --rm app python -m src.main
```

Ou via le script d'automatisation :

```bash
docker compose run --rm app sh scripts/run_pipeline.sh
```

### 3. Arrêter les services

```bash
docker compose down
```

### 4. Accéder à la base de données

```bash
docker compose run --rm app mysql --skip-ssl -h db -u gametracker -p gametracker -D gametracker
```

## Structure du projet

```
gametracker/
├── data/
│   └── raw/
│       ├── Players.csv          # Données brutes des joueurs
│       └── Scores.csv           # Données brutes des scores
├── output/
│   └── rapport.txt              # Rapport généré
├── scripts/
│   ├── init-db.sql              # Schéma de la base
│   ├── wait-for-db.sh           # Attente de la base
│   └── run_pipeline.sh          # Orchestration du pipeline
├── src/
│   ├── __init__.py
│   ├── config.py                # Configuration (variables d'env)
│   ├── database.py              # Gestion des connexions MySQL
│   ├── extract.py               # Extraction des CSV
│   ├── transform.py             # Nettoyage et transformation
│   ├── load.py                  # Chargement en base
│   ├── report.py                # Génération du rapport
│   └── main.py                  # Point d'entrée
├── Dockerfile                   # Configuration Docker
├── docker-compose.yml           # Orchestration des services
├── requirements.txt             # Dépendances Python
├── .gitignore                   # Fichiers ignorés par Git
└── README.md                    # Ce fichier
```

## Problèmes de qualité traités

### 1. **Doublons**
- Suppression des lignes entièrement dupliquées (à la fois sur player_id pour les joueurs et score_id pour les scores)
- Prévention des insertions en double via `ON DUPLICATE KEY UPDATE`

### 2. **Données manquantes**
- Gestion des valeurs NaN/NaT vers `NULL` MySQL
- Validation des emails (suppression de ceux sans `@`)
- Conversion des dates invalides en `NULL`

### 3. **Données invalides**
- Nettoyage des espaces inutiles dans les usernames (`.strip()`)
- Suppression des scores négatifs ou nuls
- Suppression des références orphelines (scores dont le player_id n'existe pas)

### 4. **Intégrité référentielle**
- Clé étrangère : `scores.player_id` → `players.player_id`
- Chargement des joueurs avant les scores

### 5. **Robustesse**
- Context manager pour gestion des connexions (commit/rollback automatique)
- Script d'attente de la base (`wait-for-db.sh`) avec retry
- Gestion des erreurs avec `set -e` dans le script Bash

### 6. **Traçabilité**
- Logs d'extraction, transformation et chargement
- Génération automatique du rapport avec statistiques détaillées
- Horodatage du rapport

## Pipeline ETL

### Extract
Lit les fichiers CSV bruts (`Players.csv`, `Scores.csv`) et retourne des DataFrames pandas.

### Transform
- **Players** : doublons, espaces, dates, emails invalides
- **Scores** : doublons, dates, scores négatifs/nuls, références orphelines

### Load
Insère les données en base avec `ON DUPLICATE KEY UPDATE` pour gérer les mises à jour.

### Report
Génère un rapport avec :
- Statistiques générales
- Top 5 des meilleurs scores
- Score moyen par jeu
- Répartition par pays
- Répartition par plateforme

## Fichiers générés

- **output/rapport.txt** : Rapport textuel avec statistiques

## Auteur

Projet réalisé dans le cadre du cours "Automatisation et test en programmation".
