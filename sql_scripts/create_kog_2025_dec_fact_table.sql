CREATE TABLE IF NOT EXISTS kog_2025_dec (
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
    CONSTRAINT fk_kog_2025_dec_player_id 
        FOREIGN KEY (player_id) 
        REFERENCES players (player_id),
    CONSTRAINT fk_kog_2025_dec_deck_id 
        FOREIGN KEY (deck_id) 
        REFERENCES decks (deck_id),
    CONSTRAINT fk_kog_2025_dec_skill_id
        FOREIGN KEY (skill_id)
        REFERENCES skills (skill_id),
    CONSTRAINT fk_kog_2025_dec_date_id
        FOREIGN KEY (date_id)
        REFERENCES calendar_2025 (date_id)
);

CREATE TRIGGER trigger_set_updated_at
BEFORE UPDATE ON kog_2025_dec
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

GRANT SELECT, INSERT, UPDATE, TRUNCATE, REFERENCES, TRIGGER ON kog_2025_dec TO usuario_que_usas;

ALTER TABLE kog_2025_dec OWNER TO usuario_que_usas;
