-- Use this SQL to completely cleanse the database. The result will be as if the database had been created again

TRUNCATE TABLE power_supply, serial_collector, fpga;

alter sequence power_supply_id_seq restart with 1;
alter sequence serial_collector_id_seq restart with 1;
alter sequence fpga_id_seq restart with 1;


-- Inserting Power Supplies
INSERT INTO power_supply (id,num,type_ps,voltage,max_current,available) VALUES (0, 0, 'USB', 5, 0.5, True);
INSERT INTO power_supply (id,num,type_ps,voltage,max_current,available) VALUES (1, 1, 'USB', 5, 0.5, True);
INSERT INTO power_supply (id,num,type_ps,voltage,max_current,available) VALUES (2, 2, 'USB', 5, 0.5, True);
INSERT INTO power_supply (id,num,type_ps,voltage,max_current,available) VALUES (3, 3, 'USB', 5, 0.5, True);
INSERT INTO power_supply (id,num,type_ps,voltage,max_current,available) VALUES (4, 4, 'USB', 5, 0.5, True);
INSERT INTO power_supply (id,num,type_ps,voltage,max_current,available) VALUES (5, 5, 'USB', 5, 0.5, True);
INSERT INTO power_supply (id,num,type_ps,voltage,max_current,available) VALUES (6, 6, 'USB', 5, 0.5, True);

-- Inserting Serial Collectors
INSERT INTO serial_collector (id,name,serial_number,type_sc,available,connected_power_supply_id) VALUES (0, 'Coletor Serial 1', null, 'EXTERNAL', True, 1);
INSERT INTO serial_collector (id,name,serial_number,type_sc,available,connected_power_supply_id) VALUES (1, 'Coletor Serial 2', null, 'EXTERNAL', True, 3);
INSERT INTO serial_collector (id,name,serial_number,type_sc,available,connected_power_supply_id) VALUES (2, 'Coletor Serial 3', null, 'INTEGRATED', True, null);

-- Inserting FPGAs
INSERT INTO fpga (id,name,manufacturer,serial_number,startup_time,available,connected_power_supply_id,connected_serial_collector_id) VALUES (0, 'Basys 2 - 100', 'Digilent', '210155296096', 2, True, 2, 1);
INSERT INTO fpga (id,name,manufacturer,serial_number,startup_time,available,connected_power_supply_id,connected_serial_collector_id) VALUES (1, 'Nexys 3 - 100', 'Digilent', '210182519945', 5, True, 4, 2);
INSERT INTO fpga (id,name,manufacturer,serial_number,startup_time,available,connected_power_supply_id,connected_serial_collector_id) VALUES (2, 'Basys 2 - 250', 'Digilent', '210155261283', 2, True, 0, 0);