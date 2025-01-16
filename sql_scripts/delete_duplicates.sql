-- Para encontrar duplicador por cargar doble el registro
WITH duplicados AS (
    SELECT player_id
    FROM kog_2025_jan
    GROUP BY player_id
    HAVING COUNT(*) > 1
)
SELECT u.*
FROM kog_2025_jan u
JOIN duplicados d ON u.player_id = d.player_id;