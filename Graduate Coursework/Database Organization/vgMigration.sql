-- First, drop tables that reference other tables
DROP TABLE IF EXISTS vg_Sales;
DROP TABLE IF EXISTS vg_GameVersion;

-- Then, drop the tables that are being referenced
DROP TABLE IF EXISTS vg_Game;
DROP TABLE IF EXISTS vg_Publisher;
DROP TABLE IF EXISTS vg_Platform;
DROP TABLE IF EXISTS vg_Genre;


-- Create Genre table
CREATE TABLE vg_Genre (
    GenreID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL
);

-- Create Platform table
CREATE TABLE vg_Platform (
    PlatformID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL
);

-- Create Publisher table
CREATE TABLE vg_Publisher (
    PublisherID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL
);

-- Modified Game table with Rank column
CREATE TABLE vg_Game (
    GameID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Year INT,
    GenreID INT,
    PlatformID INT,
    PublisherID INT,
    `Rank` INT, -- Added Rank column
    FOREIGN KEY (GenreID) REFERENCES vg_Genre(GenreID),
    FOREIGN KEY (PlatformID) REFERENCES vg_Platform(PlatformID),
    FOREIGN KEY (PublisherID) REFERENCES vg_Publisher(PublisherID)
);

-- Modified Sales table without Rank column
CREATE TABLE vg_Sales (
    SalesID INT AUTO_INCREMENT PRIMARY KEY,
    GameID INT,
    NA_Sales DOUBLE,
    EU_Sales DOUBLE,
    JP_Sales DOUBLE,
    Other_Sales DOUBLE,
    Global_Sales DOUBLE,
    FOREIGN KEY (GameID) REFERENCES vg_Game(GameID)
);


CREATE TABLE vg_GameVersion (
    VersionID INT AUTO_INCREMENT PRIMARY KEY,
    GameID INT,
    PublisherID INT,
    PlatformID INT,
    FOREIGN KEY (GameID) REFERENCES vg_Game(GameID),
    FOREIGN KEY (PublisherID) REFERENCES vg_Publisher(PublisherID),
    FOREIGN KEY (PlatformID) REFERENCES vg_Platform(PlatformID)
);


-- Data migration for Genre, Platform, and Publisher
INSERT INTO vg_Genre (Name) 
SELECT DISTINCT Genre FROM vg_csv;

INSERT INTO vg_Platform (Name) 
SELECT DISTINCT Platform FROM vg_csv;

INSERT INTO vg_Publisher (Name) 
SELECT DISTINCT Publisher FROM vg_csv;

-- Modified data migration for Game
INSERT INTO vg_Game (Name, Year, GenreID, PlatformID, PublisherID, `Rank`)
SELECT 
    vg_csv.Name, 
    CASE 
        WHEN vg_csv.Year REGEXP '^[0-9]+$' THEN vg_csv.Year
        ELSE NULL
    END AS Year,
    g.GenreID, 
    p.PlatformID, 
    pb.PublisherID,
    vg_csv.Ranking -- Added Rank column
FROM 
    vg_csv
JOIN 
    vg_Genre g ON vg_csv.Genre = g.Name
JOIN 
    vg_Platform p ON vg_csv.Platform = p.Name
JOIN 
    vg_Publisher pb ON vg_csv.Publisher = pb.Name;

-- Unchanged data migration for Sales
INSERT INTO vg_Sales (GameID, NA_Sales, EU_Sales, JP_Sales, Other_Sales, Global_Sales)
SELECT 
    gm.GameID, 
    vg_csv.NA_Sales, 
    vg_csv.EU_Sales, 
    vg_csv.JP_Sales, 
    vg_csv.Other_Sales, 
    vg_csv.Global_Sales
FROM 
    vg_csv
JOIN 
    vg_Game gm ON vg_csv.Name = gm.Name AND vg_csv.Year = gm.Year;


INSERT INTO vg_GameVersion (GameID, PublisherID, PlatformID)
SELECT 
    g.GameID, 
    p.PublisherID, 
    pl.PlatformID
FROM 
    vg_csv
JOIN 
    vg_Game g ON vg_csv.Name = g.Name 
    AND CASE 
            WHEN vg_csv.Year REGEXP '^[0-9]+$' THEN CAST(vg_csv.Year AS UNSIGNED)
            ELSE NULL
        END = g.Year
JOIN 
    vg_Publisher p ON vg_csv.Publisher = p.Name
JOIN 
    vg_Platform pl ON vg_csv.Platform = pl.Name;



select * from vg_genre;
select * from vg_platform;
select * from vg_publisher;
select * from vg_gameversion;
select * from vg_game;
select * from vg_sales;
