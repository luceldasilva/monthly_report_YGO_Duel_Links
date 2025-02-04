-- Para usar dimensión el calendario

CREATE TABLE calendar_2025 (
	date_id SERIAL PRIMARY KEY,
	ndmax DATE NOT NULL,
	day_of_monthy INT NOT NULL,
	monthy INT NOT NULL,
	weekly INT NOT NULL,
	week_of_monthy INT NOT NULL,
	monthy_name VARCHAR(15) NOT NULL
);


-- Ejemplo para cambiar de dueño
ALTER TABLE calendar_2025 OWNER TO usuario_que_usas;