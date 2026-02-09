"""Module d'extraction de données depuis les fichiers CSV."""

from pathlib import Path
import pandas as pd


def extract(filepath: str) -> pd.DataFrame:
    """Extrait les donnees d'un fichier CSV.
    
    Args:
        filepath: Chemin vers le fichier CSV.
    
    Returns:
        DataFrame contenant les donnees.
    
    Raises:
        FileNotFoundError: Si le fichier n'existe pas.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Fichier non trouve : {filepath}")
    
    df = pd.read_csv(filepath)
    print(f"Extrait {len(df)} lignes de {path.name}")
    return df
