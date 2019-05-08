-- Load the tables that contain conjugation data.
-- This script is normally executed by schema.sql.

\set ON_ERROR_STOP 1

\copy conj FROM data/conj.csv DELIMITER E'\t' CSV HEADER
\copy conjo FROM data/conjo.csv DELIMITER E'\t' CSV HEADER
\copy conotes FROM data/conotes.csv DELIMITER E'\t' CSV HEADER
\copy conjo_notes FROM data/conjo_notes.csv DELIMITER E'\t' CSV HEADER

