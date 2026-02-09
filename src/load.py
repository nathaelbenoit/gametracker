"""Module de chargement des données dans la base MySQL."""

import pandas as pd


def _to_none(value):
    """Convertit NaN/NaT en None pour MySQL."""
    if pd.isna(value):
        return None
    return value


def load_players(df: pd.DataFrame, conn) -> int:
    """Charge les joueurs dans la base de donnees.
    
    Args:
        df: DataFrame des joueurs.
        conn: Connexion MySQL.
    
    Returns:
        Nombre de lignes inserees.
    """
    cursor = conn.cursor()
    query = """
        INSERT INTO players
            (player_id, username, email, registration_date, country, level)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            username = VALUES(username),
            email = VALUES(email),
            registration_date = VALUES(registration_date),
            country = VALUES(country),
            level = VALUES(level)
    """
    
    count = 0
    for _, row in df.iterrows():
        registration_date = _to_none(row['registration_date'])
        if hasattr(registration_date, "to_pydatetime"):
            registration_date = registration_date.to_pydatetime()

        values = (
            int(row['player_id']),
            _to_none(row['username']),
            _to_none(row['email']),
            registration_date,
            _to_none(row['country']),
            _to_none(row['level'])
        )
        cursor.execute(query, values)
        count += 1
    
    print(f"Charge {count} joueurs")
    return count


def load_scores(df: pd.DataFrame, conn) -> int:
    """Charge les scores dans la base de donnees.
    
    Args:
        df: DataFrame des scores.
        conn: Connexion MySQL.
    
    Returns:
        Nombre de lignes inserees.
    """
    cursor = conn.cursor()
    query = """
        INSERT INTO scores
            (score_id, player_id, game, score, duration_minutes, played_at, platform)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            player_id = VALUES(player_id),
            game = VALUES(game),
            score = VALUES(score),
            duration_minutes = VALUES(duration_minutes),
            played_at = VALUES(played_at),
            platform = VALUES(platform)
    """
    
    count = 0
    for _, row in df.iterrows():
        played_at = _to_none(row['played_at'])
        if hasattr(played_at, "to_pydatetime"):
            played_at = played_at.to_pydatetime()

        values = (
            _to_none(row['score_id']),
            int(row['player_id']),
            _to_none(row['game']),
            int(row['score']) if pd.notna(row['score']) else None,
            _to_none(row['duration_minutes']),
            played_at,
            _to_none(row['platform'])
        )
        cursor.execute(query, values)
        count += 1
    
    print(f"Charge {count} scores")
    return count