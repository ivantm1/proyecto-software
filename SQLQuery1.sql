
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
('Medicina y Anatomía', 'Manuales clínicos, atlas anatómicos y patología'),
('Derecho Civil y Penal', 'Códigos legislativos, jurisprudencia y manuales de grado'),
('Ingeniería Informática', 'Algoritmia, bases de datos y arquitectura de sistemas'),
('Economía y Empresa', 'Microeconomía, macroeconomía y contabilidad financiera'),
('Arquitectura', 'Diseño estructural, historia del arte arquitectónico y urbanismo'),
('Biología Celular', 'Microbiología, genética y prácticas de laboratorio'),
('Física y Matemáticas', 'Cálculo avanzado, álgebra lineal y mecánica cuántica'),
('Psicología Clínica', 'Evaluación psicológica, neurociencia y terapias'),
('Historia Contemporánea', 'Archivos históricos y monografías del siglo XX'),
('Filología Moderna', 'Lingüística, gramática histórica y literatura comparada');


INSERT INTO Usuarios (contrasena, email, nombre, apellidos, tipo) VALUES 

('pass_med', 'elena.rodriguez@alumnos.univ.edu', 'Elena', 'Rodríguez', 'Estudiante'),
('pass_der', 'miguel.gomez@alumnos.univ.edu', 'Miguel', 'Gómez', 'Estudiante'),
('pass_ing', 'sara.martin@alumnos.univ.edu', 'Sara', 'Martín', 'Estudiante'),
('pass_eco', 'david.fer@alumnos.univ.edu', 'David', 'Fernández', 'Estudiante'),
('pass_arq', 'laura.diaz@alumnos.univ.edu', 'Laura', 'Díaz', 'Estudiante'),


('biblio_jefe', 'carlos.biblio@pdi.univ.edu', 'Carlos', 'López', 'Bibliotecario'),
('biblio_tarde', 'marta.biblio@pdi.univ.edu', 'Marta', 'Sánchez', 'Bibliotecario'),


('admin_root', 'sistemas.biblioteca@univ.edu', 'Admin', 'Sistemas IT', 'Admin');


INSERT INTO Estudiantes (ID_usuario, num_prestamos, num_reservas, sanciones)
SELECT ID_usuario, 0, 0, 0 
FROM Usuarios 
WHERE tipo = 'Estudiante';


INSERT INTO Libros (ISBN, titulo, autor, fecha_llegada, num_copias, disponibilidad, descripcion, nombre_tema) VALUES 

('978-84-MED', 'Anatomía con orientación clínica (Moore)', 'Keith L. Moore', '2023-09-01', 1, 'Disponible', 'Bibliografía obligatoria para 1º de Medicina', 'Medicina y Anatomía'),

('978-01-ING', 'Introduction to Algorithms (Cormen)', 'Thomas H. Cormen', '2023-09-15', 1, 'Disponible', 'El estándar mundial para el estudio de algoritmos', 'Ingeniería Informática'),

('978-33-DER', 'Código Civil Español Comentado', 'Carlos Lasarte', '2024-01-10', 1, 'Retirado', 'Edición de consulta en sala. No disponible para préstamo externo.', 'Derecho Civil y Penal'),


('978-55-ECO', 'Principios de Economía', 'N. Gregory Mankiw', '2022-09-05', 1, 'Prestado', 'Manual básico de introducción a la micro y macroeconomía', 'Economía y Empresa'),


('978-99-ARQ', 'Historia de la Arquitectura Moderna', 'Leonardo Benevolo', '2021-11-20', 1, 'Disponible', 'Edición ilustrada. Requiere trato cuidadoso.', 'Arquitectura');

GO

