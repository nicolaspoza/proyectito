CREATE TABLE clientes (
	rut VARCHAR(50) NOT NULL,
	nombre VARCHAR(50),
	telefono INTEGER NOT NULL,
	cant_libros INTEGER NOT NULL,
	password VARCHAR(255),
	PRIMARY KEY (rut),
	UNIQUE (telefono)
);
CREATE TABLE repisas (
	id INTEGER NOT NULL,
	categoria VARCHAR(50) NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (categoria)
);
CREATE TABLE empleados (
rut VARCHAR(12) NOT NULL,
nombre VARCHAR(50),
password VARCHAR(255),
PRIMARY KEY (rut)
);
CREATE TABLE libros (
	id INTEGER NOT NULL,
	nombre VARCHAR(50),
	autor VARCHAR(80),
	prestado BOOLEAN,
	id_repisa INTEGER NOT NULL,
	PRIMARY KEY (id),
	CHECK (prestado IN (0, 1)),
	FOREIGN KEY(id_repisa) REFERENCES repisas (id)
);
CREATE TABLE Presta (
	rut_cliente VARCHAR(12) NOT NULL,
	rut_empleado VARCHAR(12) NOT NULL,
	id_libro INTEGER NOT NULL,
	fecha_prest VARCHAR(9),
	fecha_dev VARCHAR(9),
	PRIMARY KEY (rut_cliente, rut_empleado, id_libro),
	FOREIGN KEY(rut_cliente) REFERENCES clientes (rut),
	FOREIGN KEY(rut_empleado) REFERENCES empleados (rut),
	FOREIGN KEY(id_libro) REFERENCES libros (id)
);


INSERT INTO Libros(Nombre, Autor, Fecha_prest, Fecha_dev, Prestado, rut_empleado, rut_cliente, ID_repisa) VALUES ('Animales Fantásticos y donde Encontrarlos', 'Newt Scamander', '05/09/2018', '10/09/2018','1', '19.954.344-k', '20.677.425-0', '35');

INSERT INTO Clientes(Rut, Nombre, Telefono, Cant_libros, Socio)
            VALUES ('20.677.425-0', 'Avril Wisley', '98757353', '3', '1');

INSERT INTO Empleados(Rut, Nombre, rut_cliente)
            VALUES ('19.954.344-k', 'Pamela Pinilla', '20.677.425-0');

INSERT INTO Repisas(ID, Categoria)
            VALUES ('35', 'Zoologia');

DELETE FROM Libros WHERE Autor='Voldemort';
DELETE FROM Clientes WHERE Socio=0;
DELETE FROM Empleados WHERE Rut='12.345.678-9';
DELETE FROM Repisas WHERE ID=54;

UPDATE Libros SET Autor= 'Lord Voldemort', Titulo= 'Maleficios Imperdonables';
UPDATE Clientes SET Nombre= "Harry Potter Carrasco", Libros=14;
UPDATE Empleados SET Rut="20.765.980-k";
UPDATE Repisas SET Categoria="Posiones";

select count(Libros.id), repisas.nombre from Libros, Repisas where Libros.id_repisa = Repisas.id Group by Repisas.nombre;
select count(libro.nombre) from Libros, Clientes where Libros.rut_cliente=Clientes.rut and Clientes.nombre="Julian Meza" and Libro.nombre="Autobiografía de Badbunn";
select count(Clientes.rut) from Cliente where Clientes.socio=1;
select count(Libros.id) from Libros, Empleados where Libros.rut_empleado = Empleados.rut and Empleados.nombre="Juanin Canzalez";
select Libros.nombre from Libros, Empleados where Empleados.rut=Libros.rut_empleados and Empleados.nombre="Maria Elza";
select Libros.nombre from Libros where Libros.ID>=1 and Libros.ID<=150;
select Libros.nombre from Libros where Libros.autor="Batman";
select Libros.autor, count(*) from Libros where Libros.nombre="Robin";
select fecha_prest from Libros, Repisas Repisas.ID=Libros.ID_repisa and Repisas.categoria="Astronomia";
select fecha_dev from Libros, Clientes where Libros.rut_cliente=Clientes.rut and Clientes.nombre="Juancho Pancho";
