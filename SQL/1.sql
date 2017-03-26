
/*
CREATE TABLE maszk 
(id integer Primary Key
,kepnev varchar
,evszam integer);

SELECT AddGeometryColumn('maszk','geom',3857,'POLYGON',2);

INSERT INTO maszk (id,geom) VALUES (1,ST_GeomFromText('POLYGON((-71.1776585052917 42.3902909739571,-71.1776820268866 42.3903701743239,
-71.1776063012595 42.3903825660754,-71.1775826583081 42.3903033653531,-71.1776585052917 42.3902909739571))',3857))

*/
SELECT * 
INTO legifoto_kozig
FROM ms WHERE telepules='Dunaújváros' 

--Különbség
DROP VIEW legifoto_nyers_fedes_1954;
CREATE VIEW legifoto_nyers_fedes_1954 AS 
SELECT 
	1 as id,ST_DIFFERENCE(ST_TRANSFORM(a.geom,3857),b.geom) as geom,'Légifotóval le nem fedett terület' as tipus

FROM
	legifoto_kozig as a,
	(SELECT 
		ST_BUFFER(ST_UNION(geom),0) as geom 
	FROM maszk  
	WHERE evszam=1954) as b
UNION 
SELECT 
	2 as id,ST_INTERSECTION(ST_TRANSFORM(a.geom,3857),b.geom)  as geom,'Légifotóval lefedett terület' as tipus
FROM
	legifoto_kozig as a,
	(SELECT 
		ST_BUFFER(ST_UNION(geom),0) as geom 
	FROM maszk  
	WHERE evszam=1954) as b

