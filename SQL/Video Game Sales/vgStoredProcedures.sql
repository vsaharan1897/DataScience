DELIMITER $$
DROP PROCEDURE IF EXISTS gameProfitByRegion$$
CREATE PROCEDURE gameProfitByRegion(IN minProfit DOUBLE, IN regionCode VARCHAR(2))
BEGIN
    IF regionCode = 'WD' THEN
        SELECT g.Name, s.Global_Sales AS Profit
        FROM vg_Game g
        JOIN vg_Sales s ON g.GameID = s.GameID
        WHERE s.Global_Sales > minProfit;
    ELSEIF regionCode = 'NA' THEN
        SELECT g.Name, s.NA_Sales AS Profit
        FROM vg_Game g
        JOIN vg_Sales s ON g.GameID = s.GameID
        WHERE s.NA_Sales > minProfit;
    ELSEIF regionCode = 'EU' THEN
        SELECT g.Name, s.EU_Sales AS Profit
        FROM vg_Game g
        JOIN vg_Sales s ON g.GameID = s.GameID
        WHERE s.EU_Sales > minProfit;
    ELSEIF regionCode = 'JP' THEN
        SELECT g.Name, s.JP_Sales AS Profit
        FROM vg_Game g
        JOIN vg_Sales s ON g.GameID = s.GameID
        WHERE s.JP_Sales > minProfit;
    END IF;
END$$

DELIMITER ;


DELIMITER $$

DROP PROCEDURE IF EXISTS genreRankingByRegion$$
CREATE PROCEDURE genreRankingByRegion(IN genreName VARCHAR(255), IN regionCode VARCHAR(2))
BEGIN
    IF regionCode = 'WD' THEN
        SELECT 
            RankedGenres.Name,
            RankedGenres.TotalSales,
            RankedGenres.Ranking
        FROM (
            SELECT 
                gr.Name,
                SUM(s.Global_Sales) AS TotalSales,
                RANK() OVER (ORDER BY SUM(s.Global_Sales) DESC) AS Ranking
            FROM 
                vg_game g
            JOIN 
                vg_sales s ON g.GameID = s.GameID
            JOIN 
                vg_genre gr ON g.GenreID = gr.GenreID
            GROUP BY 
                gr.Name
        ) AS RankedGenres
        WHERE 
            RankedGenres.Name = genreName;
    ELSEIF regionCode = 'NA' THEN
        SELECT 
            RankedGenres.Name,
            RankedGenres.TotalSales,
            RankedGenres.Ranking
        FROM (
            SELECT 
                gr.Name,
                SUM(s.NA_Sales) AS TotalSales,
                RANK() OVER (ORDER BY SUM(s.NA_Sales) DESC) AS Ranking
            FROM 
                vg_game g
            JOIN 
                vg_sales s ON g.GameID = s.GameID
            JOIN 
                vg_genre gr ON g.GenreID = gr.GenreID
            GROUP BY 
                gr.Name
        ) AS RankedGenres
        WHERE 
            RankedGenres.Name = genreName;
    ELSEIF regionCode = 'EU' THEN
        SELECT 
            RankedGenres.Name,
            RankedGenres.TotalSales,
            RankedGenres.Ranking
        FROM (
            SELECT 
                gr.Name,
                SUM(s.EU_Sales) AS TotalSales,
                RANK() OVER (ORDER BY SUM(s.EU_Sales) DESC) AS Ranking
            FROM 
                vg_game g
            JOIN 
                vg_sales s ON g.GameID = s.GameID
            JOIN 
                vg_genre gr ON g.GenreID = gr.GenreID
            GROUP BY 
                gr.Name
        ) AS RankedGenres
        WHERE 
            RankedGenres.Name = genreName;
    ELSEIF regionCode = 'JP' THEN
        SELECT 
            RankedGenres.Name,
            RankedGenres.TotalSales,
            RankedGenres.Ranking
        FROM (
            SELECT 
                gr.Name,
                SUM(s.JP_Sales) AS TotalSales,
                RANK() OVER (ORDER BY SUM(s.JP_Sales) DESC) AS Ranking
            FROM 
                vg_game g
            JOIN 
                vg_sales s ON g.GameID = s.GameID
            JOIN 
      
      vg_genre gr ON g.GenreID = gr.GenreID
            GROUP BY 
                gr.Name
        ) AS RankedGenres
        WHERE 
            RankedGenres.Name = genreName;
    END IF;
END$$

DELIMITER ;

DELIMITER $$

DROP PROCEDURE IF EXISTS publishedReleases$$
CREATE PROCEDURE publishedReleases(IN publisherName VARCHAR(255), IN genreName VARCHAR(255))
BEGIN
    SELECT 
        COUNT(*) AS TotalTitles
    FROM 
        vg_Game g
    JOIN 
        vg_Genre gr ON g.GenreID = gr.GenreID
    JOIN 
        vg_Publisher p ON g.PublisherID = p.PublisherID
    WHERE 
        gr.Name = genreName AND p.Name = publisherName;
END$$

DELIMITER ;


DELIMITER $$
DROP PROCEDURE IF EXISTS addNewRelease$$
DELIMITER $$

CREATE PROCEDURE addNewRelease(IN gameTitle VARCHAR(255), IN platformName VARCHAR(255), IN genreName VARCHAR(255), IN publisherName VARCHAR(255))
BEGIN
    DECLARE platformID INT DEFAULT 0;
    DECLARE genreID INT DEFAULT 0;
    DECLARE publisherID INT DEFAULT 0;
    DECLARE existingGameID INT DEFAULT 0;

    -- Check and insert Platform
    SELECT PlatformID INTO platformID FROM vg_Platform WHERE Name = platformName LIMIT 1;
    IF platformID = 0 THEN
        INSERT INTO vg_Platform (Name) VALUES (platformName);
        SET platformID = LAST_INSERT_ID();
    END IF;

    -- Check and insert Genre
    SELECT GenreID INTO genreID FROM vg_Genre WHERE Name = genreName LIMIT 1;
    IF genreID = 0 THEN
        INSERT INTO vg_Genre (Name) VALUES (genreName);
        SET genreID = LAST_INSERT_ID();
    END IF;

    -- Check and insert Publisher
    SELECT PublisherID INTO publisherID FROM vg_Publisher WHERE Name = publisherName LIMIT 1;
    IF publisherID = 0 THEN
        INSERT INTO vg_Publisher (Name) VALUES (publisherName);
        SET publisherID = LAST_INSERT_ID();
    END IF;

    -- Check if the game already exists
    SELECT GameID INTO existingGameID FROM vg_Game WHERE Name = gameTitle AND GenreID = genreID AND PlatformID = platformID AND PublisherID = publisherID LIMIT 1;
    IF existingGameID = 0 THEN
        -- Insert the new game release only if it does not exist
        INSERT INTO vg_Game (Name, GenreID, PlatformID, PublisherID) VALUES (gameTitle, genreID, platformID, publisherID);
        SELECT 'New game release added successfully.' AS Message;
    ELSE
        SELECT 'Game release has been added.' AS Message;
    END IF;
END$$

DELIMITER ;
