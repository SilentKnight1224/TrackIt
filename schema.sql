DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    roblox TEXT,
    riotname TEXT,
    riottag TEXT,
    steamid TEXT,
    mojangname TEXT,
    mojangpass TEXT,
    overwatchname TEXT,
    overwatchid TEXT,
    platform TEXT,
    region TEXT
);