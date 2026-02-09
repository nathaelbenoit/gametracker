"""Module de transformation des données du projet gametracker."""

import pandas as pd


def transform_players(df: pd.DataFrame) -> pd.DataFrame:
    """Transforme et nettoie les donnees des joueurs.
    
    Args:
        df: DataFrame brut des joueurs.
    
    Returns:
        DataFrame nettoye des joueurs.
    """
    df = df.copy()
    
    # Supprimer les doublons 
    df = df.drop_duplicates(subset=['player_id'])
    
    # Nettoyer les espaces du username (strip)
    df['username'] = df['username'].str.strip()

    df = df.drop_duplicates(subset=['username'])
    
    # Convertir les dates d'inscription
    df['registration_date'] = pd.to_datetime(df['registration_date'], errors='coerce')
    
    # Remplacer les emails invalides (sans @) par None
    df['email'] = df['email'].where(df['email'].str.contains('@', na=False), None)
    
    # Remplacer tous les NaN/NaT par None pour MySQL
    df = df.where(pd.notna(df), None)
    
    print(f"Transforme {len(df)} joueurs")
    return df


def transform_scores(df: pd.DataFrame, valid_player_ids: list) -> pd.DataFrame:
    """Transforme et nettoie les donnees des scores.
    
    Args:
        df: DataFrame brut des scores.
        valid_player_ids: Liste des player_id valides (sans orphelins).
    
    Returns:
        DataFrame nettoye des scores.
    """
    df = df.copy()
    
    # Supprimer les doublons
    df = df.drop_duplicates(subset=['score_id'])
    
    # Convertir les dates
    df['played_at'] = pd.to_datetime(df['played_at'], errors='coerce')
    
    # Convertir les scores en numériques
    df['score'] = pd.to_numeric(df['score'], errors='coerce')
    
    # Supprimer les lignes avec score négatif ou nul
    df = df[df['score'] > 0]
    
    # Supprimer les scores dont le player_id n'est pas valide
    df = df[df['player_id'].isin(valid_player_ids)]
    
    # Remplacer tous les NaN/NaT par None pour MySQL
    df = df.where(pd.notna(df), None)
    
    print(f"Transforme {len(df)} scores")
    return df
