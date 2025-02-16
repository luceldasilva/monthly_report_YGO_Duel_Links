-- Agregar columna de fecha para el kog de Enero

ALTER TABLE kog_2025_jan ADD COLUMN date_id INT;

ALTER TABLE kog_2025_jan 
ADD CONSTRAINT fk_kog_2025_jan_calendar 
FOREIGN KEY (date_id) REFERENCES calendar_2025(date_id);

UPDATE kog_2025_jan h
SET date_id = d.date_id
FROM calendar_2025 d
WHERE h.ndmax = d.ndmax;

ALTER TABLE kog_2025_jan DROP COLUMN ndmax;