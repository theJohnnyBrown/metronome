-- add your migration here
DROP TABLE IF EXISTS entries;
CREATE TABLE entries (
  id bigserial primary key,
  time_in timestamp,
  time_out timestamp,
  client varchar(255),
  project varchar(255),
  task varchar(255),
  notes text);
