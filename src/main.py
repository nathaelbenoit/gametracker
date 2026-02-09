"""Point d'entrée du pipeline ETL GameTracker."""

from src.config import Config
from src.database import database_connection
from src.extract import extract
from src.transform import transform_players, transform_scores
from src.load import load_players, load_scores
from src.report import generate_report


def run_pipeline():
    """Execute le pipeline ETL complet."""
    print("=" * 50)
    print("Demarrage du pipeline GameTracker")
    print("=" * 50)
    
    with database_connection() as conn:
        # ETL Players
        print("\n--- Traitement des Joueurs ---")
        df_players = extract(f"{Config.DATA_DIR}/Players.csv")
        df_players = transform_players(df_players)
        load_players(df_players, conn)
        
        # ETL Scores
        print("\n--- Traitement des Scores ---")
        df_scores = extract(f"{Config.DATA_DIR}/Scores.csv")
        valid_player_ids = df_players['player_id'].tolist()
        df_scores = transform_scores(df_scores, valid_player_ids)
        load_scores(df_scores, conn)
    
    # Rapport
    print("\n--- Generation du Rapport ---")
    generate_report()
    
    print("\n" + "=" * 50)
    print("Pipeline termine avec succes !")
    print("=" * 50)


if __name__ == '__main__':
    run_pipeline()
