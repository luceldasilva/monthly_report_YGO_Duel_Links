CREATE TABLE series (
	serie_id SERIAL PRIMARY KEY,
	serie VARCHAR(36) NOT NULL
);

CREATE TABLE characters (
	character_id SERIAL PRIMARY KEY,
	name_character VARCHAR(100) NOT NULL,
	serie_id INT,
	CONSTRAINT fk_serie
	    FOREIGN KEY (serie_id)
	    REFERENCES series(serie_id)
	    ON DELETE CASCADE
);

ALTER TABLE skills
ADD COLUMN character_id INT,
ADD CONSTRAINT fk_character
    FOREIGN KEY (character_id)
    REFERENCES characters(character_id)
    ON DELETE CASCADE;
