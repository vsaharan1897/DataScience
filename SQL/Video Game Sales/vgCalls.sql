-- Calls to game profit by region
call gameProfitByRegion(35, 'WD');
call gameProfitByRegion(12, 'EU');
call gameProfitByRegion(10, 'JP');


-- OUTPUTS--:

-- Name, Profit --
-- Mario Kart Wii	35.82 --
-- Super Mario Bros.	40.24 -- 
-- Wii Sports	82.74 --

-- Name, Profit --
-- Mario Kart Wii	12.88 --
-- Super Mario Bros.	29.02 -- 

-- Name, Profit --
-- Pokemomn Red/Pokemon Blue 10.22 --




-- Calls to genre ranking by region
call genreRankingByRegion('Sports', 'WD');
call genreRankingByRegion('Role-playing', 'NA');
call genreRankingByRegion('Role-playing', 'JP');

-- Output --
-- Name, TotalSales, Ranking --
-- Sports	3604.6200000000645	2 --

-- Name, TotalSales, Ranking --
-- Role-Playing	481.63999999999845	7 --

-- Name, TotalSales, Ranking --
-- Role-Playing	369.5299999999977	1 -- 


-- Calls to published releases
call publishedReleases('Electronic Arts', 'Sports');
call publishedReleases('Electronic Arts', 'Action');

-- OUTPUT --
-- TotalTitles --
-- 561 --

-- TotalTitles --
-- 183 --

-- Calls to add new release
call addNewRelease('Foo Attacks', 'X360', 'Strategy', 'Stevenson Studios');
-- Note that to show this works properly, you will need to perform some selects based on your table design to 
-- show that the data did in fact get inserted.





select * from vg_game where name='Foo Attacks';
-- OUTPUT --
-- GameID Name        Year     GenreID    PlatformID        PublisherID   Rank
-- 32768   Foo Attacks	NULL	     16          32	          1024       Null  11

select * from vg_platform;

-- OUTPUT --
-- PlatformID, Name --
-- 1	Wii
-- 2	NES
-- 3	GB
-- 4	DS
-- 5	X360
-- 6	PS3
-- 7	PS2
-- 8	SNES
-- 9	GBA
-- 10	3DS
-- 11	PS4
-- 12	N64
-- 13	PS
-- 14	XB
-- 15	PC
-- 16	2600
-- 17	PSP
-- 18	XOne
-- 19	GC
-- 20	WiiU
-- 21	GEN
-- 22	DC
-- 23	PSV
-- 24	SAT
-- 25	SCD
-- 26	WS
-- 27	NG
-- 28	TG16
-- 29	3DO
-- 30	GG
-- 31	PCFX
-- 32	X360

	
select * from vg_genre;

-- OUTPUT --
-- GenreID, Name --
-- 1	Sports
-- 2	Platform
-- 3	Racing
-- 4	Role-Playing
-- 5	Puzzle
-- 6	Misc
-- 7	Shooter
-- 8	Simulation
-- 9	Action
-- 10	Fighting
-- 11	Adventure
-- 12	Strategy
-- 16	Strategy

	
select * from vg_publisher where name ='Stevenson Studios';

-- OUTPUT--
-- PublisherID, Name --
-- 1024	Stevenson Studios










