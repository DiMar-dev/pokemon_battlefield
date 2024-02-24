CREATE TABLE IF NOT EXISTS dim_move (
    id SERIAL  PRIMARY KEY,
    name VARCHAR(100) UNIQUE,
    power INT
);

CREATE TABLE IF NOT EXISTS dim_pokemon (
    id SERIAL PRIMARY KEY,
    poke_id INT UNIQUE,
    name VARCHAR(100),
    speed INT
);

CREATE TABLE IF NOT EXISTS dim_stat (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    change VARCHAR(100),
    move_id INT,
    FOREIGN KEY (move_id) REFERENCES dim_move(id)
);

ALTER TABLE dim_stat ADD CONSTRAINT name_move_id_unique UNIQUE (name, move_id);

CREATE TABLE IF NOT EXISTS fact_attack (
    id SERIAL PRIMARY KEY,
    stat_changed FLOAT,
    effort_ev INT,
    stat_id INT,
    move_id INT,
    iv FLOAT,
    level INT,
    nature_modifier FLOAT,
    pokemon_id INT,
    hp INT,
    FOREIGN KEY (stat_id) REFERENCES dim_stat(id),
    FOREIGN KEY (move_id) REFERENCES dim_move(id),
    FOREIGN KEY (pokemon_id) REFERENCES dim_pokemon(id)
);

CREATE TABLE IF NOT EXISTS fact_battle (
    id SERIAL PRIMARY KEY,
    timestamp_ TIMESTAMP DEFAULT NOW(),
    pokemon_id_1 INT,
    pokemon_id_2 INT,
    attack_pokemon_id_1 INT,
    attack_pokemon_id_2 INT,
    battle_duration_s INT,
    winner_pokemon_id INT,
    FOREIGN KEY (pokemon_id_1) REFERENCES dim_pokemon(id),
    FOREIGN KEY (pokemon_id_2) REFERENCES dim_pokemon(id),
    FOREIGN KEY (attack_pokemon_id_1) REFERENCES fact_attack(id),
    FOREIGN KEY (attack_pokemon_id_2) REFERENCES fact_attack(id),
    FOREIGN KEY (winner_pokemon_id) REFERENCES dim_pokemon(id)
);
