"""Module de génération de rapport pour GameTracker."""

from datetime import datetime
import os

from src.database import database_connection


def generate_report() -> str:
	"""Génère un rapport de synthèse et l'écrit dans output/rapport.txt.

	Returns:
		Chemin du fichier de rapport généré.
	"""
	report_lines = []
	now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	separator = "=" * 52

	with database_connection() as conn:
		cur = conn.cursor()

		# Statistiques générales
		cur.execute("SELECT COUNT(*) FROM players")
		total_players = cur.fetchone()[0]

		cur.execute("SELECT COUNT(*) FROM scores")
		total_scores = cur.fetchone()[0]

		cur.execute("SELECT COUNT(DISTINCT game) FROM scores")
		total_games = cur.fetchone()[0]

		# Top 5 des meilleurs scores
		cur.execute(
			"""
			SELECT p.username, s.game, s.score
			FROM scores s
			JOIN players p ON s.player_id = p.player_id
			ORDER BY s.score DESC
			LIMIT 5
			"""
		)
		top_scores = cur.fetchall()

		# Score moyen par jeu
		cur.execute(
			"""
			SELECT game, AVG(score) AS avg_score
			FROM scores
			GROUP BY game
			ORDER BY game
			"""
		)
		avg_scores = cur.fetchall()

		# Répartition des joueurs par pays
		cur.execute(
			"""
			SELECT country, COUNT(*) AS count_players
			FROM players
			GROUP BY country
			ORDER BY count_players DESC, country
			"""
		)
		players_by_country = cur.fetchall()

		# Répartition des sessions par plateforme
		cur.execute(
			"""
			SELECT platform, COUNT(*) AS count_sessions
			FROM scores
			GROUP BY platform
			ORDER BY count_sessions DESC, platform
			"""
		)
		sessions_by_platform = cur.fetchall()

	report_lines.append(separator)
	report_lines.append("GAMETRACKER - Rapport de synthese")
	report_lines.append(f"Genere le : {now}")
	report_lines.append(separator)
	report_lines.append("--- Statistiques generales ---")
	report_lines.append(f"Nombre de joueurs : {total_players}")
	report_lines.append(f"Nombre de scores : {total_scores}")
	report_lines.append(f"Nombre de jeux : {total_games}")

	report_lines.append("--- Top 5 des meilleurs scores ---")
	for idx, (username, game, score) in enumerate(top_scores, start=1):
		report_lines.append(f"{idx}. {username} | {game} | {score}")

	report_lines.append("--- Score moyen par jeu ---")
	for game, avg_score in avg_scores:
		report_lines.append(f"{game} : {avg_score:.1f}")

	report_lines.append("--- Joueurs par pays ---")
	for country, count_players in players_by_country:
		report_lines.append(f"{country} : {count_players}")

	report_lines.append("--- Sessions par plateforme ---")
	for platform, count_sessions in sessions_by_platform:
		report_lines.append(f"{platform} : {count_sessions}")

	report_lines.append(separator)

	output_dir = os.path.join("/app", "output")
	os.makedirs(output_dir, exist_ok=True)
	report_path = os.path.join(output_dir, "rapport.txt")

	with open(report_path, "w", encoding="utf-8") as f:
		f.write("\n".join(report_lines))

	print(f"Rapport généré : {report_path}")
	return report_path
