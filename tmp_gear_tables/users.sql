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
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: cottrillad
--

INSERT INTO auth_user VALUES (2, 'pbkdf2_sha256$20000$ABrDeJrmE2sE$cinN45NdUH8wO2lVh9yDTBM+cruJJTkeXoJIBlbBdTE=', NULL, false, 'speersje', 'Jeff', 'Speers', 'jeff.speers@ontario.ca', false, true, '2016-10-24 06:52:31-04');
INSERT INTO auth_user VALUES (6, 'pbkdf2_sha256$20000$LePQlL7jCYxG$Zf9M4A5TIfu8rzMGzea7eiqX0agRe+26AF5ZJfgBb7A=', NULL, false, 'wilsonda', 'Darrel', 'Wilson', 'darrel.wilson@ontario.ca', false, true, '2016-10-24 06:53:46-04');
INSERT INTO auth_user VALUES (4, 'pbkdf2_sha256$20000$pttEjVtQ3Ctl$I0tiZrISq5LbAdbV6T0oUJMoGzVvO3NnW202w5Kp5xg=', NULL, false, 'davisch', 'Chris', 'Davis', 'chris.davis@ontario.ca', false, true, '2016-10-24 06:53:24-04');
INSERT INTO auth_user VALUES (3, 'pbkdf2_sha256$20000$BTiOBAzc1bQI$p4BUaa64qwJViSnIub4SJ9/7Pr/GKgU9rdLbMHKzE24=', NULL, false, 'gilest', 'Steve', 'Gile', 'steve.gile@ontario.ca', false, true, '2016-10-24 06:53:14-04');
INSERT INTO auth_user VALUES (5, 'pbkdf2_sha256$20000$XJorSVGJvg2y$4Iid7O6aCYSNIpfFuD0RmLKz72/zT+upOR3eNmADcgw=', NULL, false, 'leevi', 'Vicki', 'Lee', 'vicki.lee@ontario.ca', false, true, '2016-10-24 06:53:36-04');
INSERT INTO auth_user VALUES (1, 'pbkdf2_sha256$20000$4x3DwQJtuaTr$q+JUjXrOrqo7fE8GuGdIAU1+eDsyRXxfwO5TINJuYIU=', '2016-10-24 06:51:58-04', true, 'cottrillad', 'Adam', 'Cottrill', 'racottrill@gmail.com', true, true, '2016-10-24 06:51:48-04');
INSERT INTO auth_user VALUES (7, 'pbkdf2_sha256$20000$1x3EEjjbhLXA$4Wo8flDpa3j9750JtXrWwoFi4KNm6wajetYfdw+lD8s=', NULL, false, 'liskauskasar', 'Arunas', 'Liskauskas', 'arunas.liskauskas@ontario.ca', false, true, '2016-10-24 07:38:32-04');


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cottrillad
--

SELECT pg_catalog.setval('auth_user_id_seq', 7, true);


--
-- PostgreSQL database dump complete
--

