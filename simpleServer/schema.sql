-- from server import init_db
-- init_db()

CREATE TABLE user(id INTEGER PRIMARY KEY, name TEXT, code TEXT);

CREATE TABLE userAccess(id INTEGER PRIMARY KEY, user INTEGER, device INTEGER, level INTEGER);

CREATE TABLE device(id INTEGER PRIMARY KEY, name TEXT, description TEXT);

insert into device (id, name, description) values (0, 'laser cutter', '80w laser cutter');
insert into device (id, name, description) values (1, '3d printer', 'fancy 3d printer');

insert into user (id, name, code) values (0, 'matt', 'abcde');
insert into user (id, name, code) values (1, 'ron', 'abcdesdf');

insert into userAccess(id, user, device, level) values(0,0,0,1);
insert into userAccess(id, user, device, level) values(1,0,1,1);
insert into userAccess(id, user, device, level) values(2,1,0,2);
