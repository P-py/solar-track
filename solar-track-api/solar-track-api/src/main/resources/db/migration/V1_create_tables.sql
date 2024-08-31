CREATE TABLE solar_cell_station(
    id SERIAL PRIMARY KEY,
    name VARCHAR(40)
);

CREATE TABLE solar_track_data(
    id SERIAL PRIMARY KEY,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    solar_radiation REAL NOT NULL,
    datetime TIMESTAMP WITHOUT TIME ZONE NOT NULL,
);

ALTER TABLE solar_track_data
    ADD COLUMN solar_cell_id INT
    CONSTRAINT solar_cell_fk_id
    REFERENCES solar_cell_station(id)
    ON UPDATE CASCADE ON DELETE CASCADE;