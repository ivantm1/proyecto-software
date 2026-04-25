
CREATE DATABASE BibliotecaDB;
GO

USE BibliotecaDB;
GO


CREATE TABLE Tema (
    nombre_tema VARCHAR(100) PRIMARY KEY ,
    descripcion VARCHAR(255) 
);

CREATE TABLE Usuarios (
    ID_usuario INT PRIMARY KEY IDENTITY(1,1),
    contrasena VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    nombre VARCHAR(50),
	apellidos VARCHAR(50),
    tipo VARCHAR(20) CHECK (tipo IN ('Estudiante', 'Bibliotecario', 'Admin')) 
);


CREATE TABLE Estudiantes (
    ID_usuario INT PRIMARY KEY,
    num_prestamos INT DEFAULT 0,
    num_reservas INT DEFAULT 0,
	sanciones INT DEFAULT 0,
    FOREIGN KEY (ID_usuario) REFERENCES Usuarios(ID_usuario) ON DELETE CASCADE
);



CREATE TABLE Notificaciones (
    ID_notificacion INT PRIMARY KEY IDENTITY(1,1),
    mensaje TEXT NOT NULL,
    fecha_envio DATETIME DEFAULT GETDATE(),
    ID_usuario INT,
    FOREIGN KEY (ID_usuario) REFERENCES Estudiantes(ID_usuario) ON DELETE CASCADE
);

CREATE TABLE Libros (
    ISBN VARCHAR(20) PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    autor VARCHAR(100) NOT NULL,
    fecha_llegada DATE,
	num_copias INT default 1,
	disponibilidad VARCHAR(40) CHECK (disponibilidad IN ('Disponible', 'Retirado', 'Prestado')),
    descripcion TEXT,
    nombre_tema VARCHAR(100),
    FOREIGN KEY (nombre_tema) REFERENCES Tema(nombre_tema)
);


CREATE TABLE Sanciones (
    ID_sancion INT PRIMARY KEY IDENTITY(1,1),
    tipo VARCHAR(100) NOT NULL,
	estado VARCHAR(40) CHECK (estado IN ('Activa', 'Cumplida')),
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    ID_usuario INT, 
    FOREIGN KEY (ID_usuario) REFERENCES Estudiantes(ID_usuario) ON DELETE CASCADE
);


CREATE TABLE Reservas (
	ID_reserva INT PRIMARY KEY IDENTITY(1,1),
	estado VARCHAR(40) CHECK (estado IN ('Pendiente', 'Cumplida')) default 'Pendiente' ,
    ID_usuario INT,
    ISBN VARCHAR(20),
    fecha_reserva DATE NOT NULL,
    FOREIGN KEY (ID_usuario) REFERENCES Estudiantes(ID_usuario),
    FOREIGN KEY (ISBN) REFERENCES Libros(ISBN)
);

CREATE TABLE Prestamos (
	ID_prestamo INT PRIMARY KEY IDENTITY(1,1),
    ID_usuario INT,
    ISBN VARCHAR(20),
	estado VARCHAR(40) CHECK (estado IN ('Activo', 'Devuelto', 'Vencido')),
    fecha_prestamo DATE NOT NULL,
    fecha_devolucion DATE NOT NULL,
	prorroga BIT default 0,
    FOREIGN KEY (ID_usuario) REFERENCES Estudiantes(ID_usuario),
    FOREIGN KEY (ISBN) REFERENCES Libros(ISBN)
);
GO





USE BibliotecaDB;
GO


INSERT INTO Tema (nombre_tema, descripcion) VALUES 
('Medicina y Anatom�a', 'Manuales cl�nicos, atlas anat�micos y patolog�a'),
('Derecho Civil y Penal', 'C�digos legislativos, jurisprudencia y manuales de grado'),
('Ingenier�a Inform�tica', 'Algoritmia, bases de datos y arquitectura de sistemas'),
('Econom�a y Empresa', 'Microeconom�a, macroeconom�a y contabilidad financiera'),
('Arquitectura', 'Dise�o estructural, historia del arte arquitect�nico y urbanismo'),
('Biolog�a Celular', 'Microbiolog�a, gen�tica y pr�cticas de laboratorio'),
('F�sica y Matem�ticas', 'C�lculo avanzado, �lgebra lineal y mec�nica cu�ntica'),
('Psicolog�a Cl�nica', 'Evaluaci�n psicol�gica, neurociencia y terapias'),
('Historia Contempor�nea', 'Archivos hist�ricos y monograf�as del siglo XX'),
('Filolog�a Moderna', 'Ling��stica, gram�tica hist�rica y literatura comparada');


INSERT INTO Usuarios (contrasena, email, nombre, apellidos, tipo) VALUES 

('1234', 'estudiante1@estudiantes.unileon.es', 'Elena', 'Rodr�guez', 'Estudiante'),
('pass_der', 'miguel.gomez@estudiantes.unileon.es', 'Miguel', 'G�mez', 'Estudiante'),
('pass_ing', 'sara.martin@estudiantes.unileon.es', 'Sara', 'Mart�n', 'Estudiante'),
('pass_eco', 'david.fer@estudiantes.unileon.es', 'David', 'Fern�ndez', 'Estudiante'),
('pass_arq', 'laura.diaz@estudiantes.unileon.es', 'Laura', 'D�az', 'Estudiante'),


('biblio_jefe', 'carlos.biblio@unileon.es', 'Carlos', 'L�pez', 'Bibliotecario'),
('biblio_tarde', 'marta.biblio@unileon.es', 'Marta', 'S�nchez', 'Bibliotecario'),


('admin_root', 'sistemas.biblioteca@unileon.es', 'Admin', 'Sistemas IT', 'Admin');


INSERT INTO Estudiantes (ID_usuario, num_prestamos, num_reservas, sanciones)
SELECT ID_usuario, 0, 0, 0 
FROM Usuarios 
WHERE tipo = 'Estudiante';
ALTER LOGIN biblioteca_user WITH PASSWORD = 'pruebaISD2024';
ALTER LOGIN biblioteca_user ENABLE;


INSERT INTO Libros (ISBN, titulo, autor, fecha_llegada, num_copias, disponibilidad, descripcion, nombre_tema) VALUES 

('978-84-MED', 'Anatom�a con orientaci�n cl�nica (Moore)', 'Keith L. Moore', '2023-09-01', 1, 'Disponible', 'Bibliograf�a obligatoria para 1� de Medicina', 'Medicina y Anatom�a'),

('978-01-ING', 'Introduction to Algorithms (Cormen)', 'Thomas H. Cormen', '2023-09-15', 1, 'Disponible', 'El est�ndar mundial para el estudio de algoritmos', 'Ingenier�a Inform�tica'),

('978-33-DER', 'C�digo Civil Espa�ol Comentado', 'Carlos Lasarte', '2024-01-10', 1, 'Retirado', 'Edici�n de consulta en sala. No disponible para pr�stamo externo.', 'Derecho Civil y Penal'),


('978-55-ECO', 'Principios de Econom�a', 'N. Gregory Mankiw', '2022-09-05', 1, 'Prestado', 'Manual b�sico de introducci�n a la micro y macroeconom�a', 'Econom�a y Empresa'),


('978-99-ARQ', 'Historia de la Arquitectura Moderna', 'Leonardo Benevolo', '2021-11-20', 1, 'Disponible', 'Edici�n ilustrada. Requiere trato cuidadoso.', 'Arquitectura');

GO

