
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
    nombre_user VARCHAR(50) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    first_name VARCHAR(50),
    full_name VARCHAR(100),
    tipo VARCHAR(20) CHECK (tipo IN ('Estudiante', 'Bibliotecario', 'Admin')) 
);


CREATE TABLE Estudiantes (
    ID_usuario INT PRIMARY KEY,
    num_prestamos INT DEFAULT 0,
    num_reservas INT DEFAULT 0,
    FOREIGN KEY (ID_usuario) REFERENCES Usuarios(ID_usuario) ON DELETE CASCADE
);

CREATE TABLE Bibliotecarios (
    ID_usuario INT PRIMARY KEY,
    FOREIGN KEY (ID_usuario) REFERENCES Usuarios(ID_usuario) ON DELETE CASCADE
);

CREATE TABLE Admins (
    ID_usuario INT PRIMARY KEY,
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
    descripcion TEXT,
    nombre_tema VARCHAR(100),
    FOREIGN KEY (nombre_tema) REFERENCES Tema(nombre_tema)
);

CREATE TABLE Ejemplar (
    ID_ejemplar INT PRIMARY KEY IDENTITY(1,1),
    estado_conservacion VARCHAR(100),
    ISBN VARCHAR(20),
    FOREIGN KEY (ISBN) REFERENCES Libros(ISBN) ON DELETE CASCADE
);

CREATE TABLE Sanciones (
    ID_sancion INT PRIMARY KEY IDENTITY(1,1),
    tipo VARCHAR(100) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    ID_usuario INT, 
    FOREIGN KEY (ID_usuario) REFERENCES Estudiantes(ID_usuario) ON DELETE CASCADE
);


CREATE TABLE Reservas (
    ID_usuario INT,
    ISBN VARCHAR(20),
    fecha_reserva DATE NOT NULL,
    PRIMARY KEY (ID_usuario, ISBN, fecha_reserva),
    FOREIGN KEY (ID_usuario) REFERENCES Estudiantes(ID_usuario),
    FOREIGN KEY (ISBN) REFERENCES Libros(ISBN)
);

CREATE TABLE Prestamos (
    ID_usuario INT,
    ID_ejemplar INT,
    fecha_prestamo DATE NOT NULL,
    fecha_devolucion_max DATE NOT NULL,
    fecha_devolucion_real DATE,
    PRIMARY KEY (ID_usuario, ID_ejemplar, fecha_prestamo),
    FOREIGN KEY (ID_usuario) REFERENCES Estudiantes(ID_usuario),
    FOREIGN KEY (ID_ejemplar) REFERENCES Ejemplar(ID_ejemplar)
);
GO

USE BibliotecaDB;
GO


INSERT INTO Tema (nombre_tema, descripcion) VALUES 
('Programación', 'Libros sobre desarrollo de software y algoritmos'),
('Base de Datos', 'Teoría y práctica de SQL y NoSQL'),
('Inteligencia Artificial', 'Redes neuronales y aprendizaje automático'),
('Historia', 'Crónicas y relatos históricos universales'),
('Novela', 'Literatura de ficción y narrativa');


INSERT INTO Usuarios (nombre_user, contrasena, email, first_name, full_name, tipo) VALUES 
('juan_perez', 'pass123', 'juan@email.com', 'Juan', 'Juan Pérez', 'Estudiante'),
('maria_garcia', 'pass456', 'maria@email.com', 'Maria', 'Maria García', 'Estudiante'),
('carlos_ruiz', 'pass789', 'carlos@email.com', 'Carlos', 'Carlos Ruiz', 'Estudiante'),
('ana_lopez', 'passabc', 'ana@email.com', 'Ana', 'Ana López', 'Estudiante'),
('luis_mesa', 'passdef', 'luis@email.com', 'Luis', 'Luis Mesa', 'Estudiante'),
('biblio_pedro', 'sec1', 'pedro@biblioteca.com', 'Pedro', 'Pedro Bibliotecario', 'Bibliotecario'),
('biblio_elena', 'sec2', 'elena@biblioteca.com', 'Elena', 'Elena Bibliotecaria', 'Bibliotecario'),
('admin_root', 'admin2024', 'admin@biblioteca.com', 'Admin', 'Administrador General', 'Admin');


INSERT INTO Estudiantes (ID_usuario, num_prestamos, num_reservas) VALUES 
(1, 0, 0), (2, 0, 0), (3, 0, 0), (4, 0, 0), (5, 0, 0);


INSERT INTO Libros (ISBN, titulo, autor, fecha_llegada, descripcion, nombre_tema) VALUES 
('978-01', 'Código Limpio', 'Robert C. Martin', '2023-01-15', 'Manual de buenas prácticas', 1),
('978-02', 'SQL para Principiantes', 'Itzik Ben-Gan', '2023-02-10', 'Guía básica de consultas', 2),
('978-03', 'Deep Learning', 'Ian Goodfellow', '2023-05-20', 'Libro avanzado sobre IA', 3),
('978-04', 'Don Quijote', 'Miguel de Cervantes', '2022-12-01', 'Clásico de la literatura', 5);


INSERT INTO Ejemplar (estado_conservacion, ISBN) VALUES 
('Nuevo', '978-01'), ('Bueno', '978-02'), ('Nuevo', '978-03'), ('Excelente', '978-04');

GO
