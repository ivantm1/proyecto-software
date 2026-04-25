
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


