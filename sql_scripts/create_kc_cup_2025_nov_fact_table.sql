CREATE TABLE IF NOT EXISTS kc_cup_2025_nov (
    id SERIAL PRIMARY KEY,
    player_id INT NOT NULL,
    deck_id INT NOT NULL,
    skill_id INT NOT NULL,
    date_id INT NOT NULL,
    zerotg BOOLEAN NOT NULL,
    zephra BOOLEAN NOT NULL,
    bryan BOOLEAN NOT NULL,
    xenoblur BOOLEAN NOT NULL,
    yamiglen BOOLEAN NOT NULL,
    latino_vania BOOLEAN NOT NULL,
    updater_label VARCHAR(32) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT fk_kc_cup_2025_nov_player_id 
        FOREIGN KEY (player_id) 
        REFERENCES players (player_id),
    CONSTRAINT fk_kc_cup_2025_nov_deck_id 
        FOREIGN KEY (deck_id) 
        REFERENCES decks (deck_id),
    CONSTRAINT fk_kc_cup_2025_nov_skill_id
        FOREIGN KEY (skill_id)
        REFERENCES skills (skill_id),
    CONSTRAINT fk_kc_cup_2025_nov_date_id
        FOREIGN KEY (date_id)
        REFERENCES calendar_2025 (date_id)
);

CREATE TRIGGER trigger_set_updated_at
BEFORE UPDATE ON kc_cup_2025_nov
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

GRANT SELECT, INSERT, UPDATE, TRUNCATE, REFERENCES, TRIGGER ON kc_cup_2025_nov TO usuario_que_usas;

ALTER TABLE kc_cup_2025_nov OWNER TO usuario_que_usas;
