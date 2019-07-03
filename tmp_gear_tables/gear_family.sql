--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

--
-- Data for Name: fn_portal_gearfamily; Type: TABLE DATA; Schema: public; Owner: cottrillad
--

INSERT INTO fn_portal_gearfamily VALUES (1, 'Trap Net', 'TP', 'TP');
INSERT INTO fn_portal_gearfamily VALUES (2, 'Bottle trap', 'BOT', 'XX');
INSERT INTO fn_portal_gearfamily VALUES (3, 'CORA Large-mesh nets', 'CORA', 'GL');
INSERT INTO fn_portal_gearfamily VALUES (4, 'Electrofishing', 'EL', 'EL');
INSERT INTO fn_portal_gearfamily VALUES (5, 'Fyke Net', 'FY', 'FY');
INSERT INTO fn_portal_gearfamily VALUES (6, 'GEE Minnow Trap', 'GEE', 'MN');
INSERT INTO fn_portal_gearfamily VALUES (7, 'Gill Net', 'GL', 'GL');
INSERT INTO fn_portal_gearfamily VALUES (8, 'Offshore Index Multifilament', 'OSIA-Multi', 'GL');
INSERT INTO fn_portal_gearfamily VALUES (9, 'Offshore Index Monofilament', 'OSIA-Mono', 'GL');
INSERT INTO fn_portal_gearfamily VALUES (10, 'SLIN Gear', 'SLIN-FLIN', 'GL');
INSERT INTO fn_portal_gearfamily VALUES (11, 'Fall Walleye Index Netting Gear', 'FWIN', 'GL');
INSERT INTO fn_portal_gearfamily VALUES (12, 'Hoop Net', 'HP', 'HP');
INSERT INTO fn_portal_gearfamily VALUES (13, 'North American Standard Index Gear', 'NA1', 'GL');
INSERT INTO fn_portal_gearfamily VALUES (14, 'Nordic Index Net', 'NOR', 'GL');
INSERT INTO fn_portal_gearfamily VALUES (15, 'Ontario BSM Standard Index Gear', 'ON2', 'GL');
INSERT INTO fn_portal_gearfamily VALUES (16, 'Beach Seine', 'SE', 'SE');
INSERT INTO fn_portal_gearfamily VALUES (17, 'Ontario Smallfish Index Gear (short)', 'SIN1', 'GL');
INSERT INTO fn_portal_gearfamily VALUES (18, 'Ontario Smallfish Index Gear (tall)', 'SIN2', 'GL');
INSERT INTO fn_portal_gearfamily VALUES (19, 'Trawl', 'TWL', 'TW');
INSERT INTO fn_portal_gearfamily VALUES (20, 'Windermere Trap', 'WIN', 'WD');


--
-- Name: fn_portal_gearfamily_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cottrillad
--

SELECT pg_catalog.setval('fn_portal_gearfamily_id_seq', 20, true);


--
-- PostgreSQL database dump complete
--

