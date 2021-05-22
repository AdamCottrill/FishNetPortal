-- CREATE our function first 

-- create our group and give them
-- appropiate privledges, including access to each of our queries

-- create our user and add them to our group.

-- GLB READONLY
CREATE ROLE glb_readonly;

GRANT CONNECT
  ON database gldjango
  TO glb_readonly;

GRANT USAGE
  ON schema PUBLIC
  TO glb_readonly;

GRANT SELECT
  ON all sequences IN SCHEMA PUBLIC
  TO glb_readonly;

GRANT SELECT
  ON all tables IN SCHEMA PUBLIC
  TO glb_readonly;

commit;
  



-- we will need to add functions to this list as they are created (and
-- may need to add functions with different call signatures).
GRANT EXECUTE
  ON FUNCTION fn011(varchar)
  TO glb_readonly;


GRANT EXECUTE
  ON FUNCTION fn121(varchar)
  TO glb_readonly;


GRANT EXECUTE
  ON FUNCTION fn122(varchar)
  TO glb_readonly;

GRANT EXECUTE
  ON FUNCTION fn123(varchar)
  TO glb_readonly;

GRANT EXECUTE
  ON FUNCTION fn125(varchar)
  TO glb_readonly;

commit;

--888888888888888888888888888888888


CREATE USER glb_user
WITH password 'fwsb2020';

-- add our user to our group
GRANT glb_readonly
  TO glb_user;

commit;

