-- Agregar tipos de habilidades
INSERT INTO skill_types (skill_type)
VALUES
	('Legendaria'),
	('De Archivo');
REVOKE INSERT, UPDATE, DELETE ON public.skill_types FROM PUBLIC;

-- Agregar series de Yu-Gi-Oh!
INSERT INTO series (serie)
VALUES
	('Duel Monsters'),
	('GX'),
	('5Ds'),
	('DSOD'),
	('ZEXAL'),
	('ARC-V'),
	('VRAINS'),
	('SEVENS'),
	('GO-RUSH');

-- Agregar personaje Vagabundo
INSERT INTO characters (name_character, serie_id)
VALUES
	('Vagabundo', 1);

-- Agregar Habilidad no asingnada
INSERT INTO skills (skill_type_id , skill, character_id)
VALUES (1, 'Habilidad no asignada', 1)