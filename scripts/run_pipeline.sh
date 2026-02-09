#!/bin/sh

set -e

echo "[1/4] Attente de la base de données..."
./scripts/wait-for-db.sh

echo "[2/4] Initialisation des tables..."
mysql --skip-ssl -h "${DB_HOST}" -P "${DB_PORT}" -u "${DB_USER}" -p"${DB_PASSWORD}" "${DB_NAME}" < /app/scripts/init-db.sql

echo "[3/4] Exécution du pipeline ETL..."
python -c "import textwrap; exec(textwrap.dedent('''
from src.extract import extract
from src.transform import transform_players, transform_scores
from src.load import load_players, load_scores
from src.database import get_connection

players_df = extract('/app/data/raw/Players.csv')
scores_df = extract('/app/data/raw/Scores.csv')
players_t = transform_players(players_df)
valid_ids = players_t['player_id'].tolist()
scores_t = transform_scores(scores_df, valid_ids)

conn = get_connection()
load_players(players_t, conn)
load_scores(scores_t, conn)
conn.commit()
conn.close()
'''))"

echo "[4/4] Génération du rapport..."
python -c "from src.report import generate_report; generate_report()"

echo "Pipeline terminé avec succès."
