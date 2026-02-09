-- Schéma de la base gametracker

CREATE TABLE IF NOT EXISTS players (
    player_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(200),
    registration_date DATETIME,
    country VARCHAR(100),
    level INT
);

CREATE TABLE IF NOT EXISTS scores (
    score_id VARCHAR(20) PRIMARY KEY,
    player_id INT NOT NULL,
    game VARCHAR(100),
    score INT NOT NULL,
    duration_minutes INT,
    played_at DATETIME,
    platform VARCHAR(50),
    CONSTRAINT fk_scores_players
        FOREIGN KEY (player_id) REFERENCES players(player_id)
);
