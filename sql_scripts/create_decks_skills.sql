SET CLIENT_ENCODING TO 'UTF8';

CREATE TABLE decks (
	deck_id SERIAL PRIMARY KEY,
	deck VARCHAR(100) NOT NULL
);

CREATE TABLE skill_types (
	skill_type_id SERIAL PRIMARY KEY,
	skill_type VARCHAR(16) NOT NULL
);

CREATE TABLE skills (
	skill_id SERIAL PRIMARY KEY,
	skill_type_id INT NOT NULL,
	skill VARCHAR(255) NOT NULL,
    CONSTRAINT fk_skill_type
	    FOREIGN KEY (skill_type_id)
	    REFERENCES skill_types(skill_type_id)
	    ON DELETE CASCADE
);

SET datestyle TO 'European';