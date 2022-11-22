CREATE TABLE events_nfl (
    event_id SERIAL PRIMARY KEY,
    event_date date NOT NULL,
    event_time time NOT NULL,
    away_team_id varchar(50) NOT NULL,
    away_nick_name varchar(100) NOT NULL,
    away_city varchar(100) NOT NULL,
    away_rank integer NOT NULL,
    away_rank_points real NOT NULL,
    home_team_id varchar(50) NOT NULL,
    home_nick_name varchar(100) NOT NULL,
    home_city varchar(100) NOT NULL,
    home_rank integer NOT NULL,
    home_rank_points real NOT NULL
);

CREATE UNIQUE INDEX event_index ON events_nfl (event_id);