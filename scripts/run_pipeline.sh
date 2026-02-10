#!/bin/bash
# Script de lancement du pipeline ETL
set -e

echo "Attente de la base de donnees..."
./scripts/wait-for-db.sh

echo "Initialisation des tables..."
mysql --skip-ssl -h "${DB_HOST}" -P "${DB_PORT}" -u "${DB_USER}" -p"${DB_PASSWORD}" "${DB_NAME}" < scripts/init-db.sql

echo "Execution du pipeline ETL..."
python -m src.main

echo "Pipeline termine avec succes !"
