-- from server import init_db
-- init_db()

CREATE TABLE user(id INTEGER PRIMARY KEY, name TEXT, code TEXT);

CREATE TABLE userAccess(id INTEGER PRIMARY KEY, user INTEGER, device INTEGER, level INTEGER, trainer INTEGER, datecreated TEXT, datemodified TEXT);

CREATE TABLE device(id INTEGER PRIMARY KEY, name TEXT, description TEXT);

insert into device (id, name, description) values (0, 'laser cutter', '80w laser cutter');
insert into device (id, name, description) values (1, '3d printer', 'fancy 3d printer');

insert into user (id, name, code) values (0, 'matt', '04001D4868');
insert into user (id, name, code) values (1, 'ron', '150060E726');

insert into userAccess(id, user, device, level) values(0,0,0,1,1,datetime('now'),datetime('now'));
insert into userAccess(id, user, device, level) values(1,0,1,2,1,datetime('now'),datetime('now'));
insert into userAccess(id, user, device, level) values(2,1,0,1,1,datetime('now'),datetime('now'));
