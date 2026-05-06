USE master;
GO

IF EXISTS (SELECT name FROM sys.databases WHERE name = 'BibliotecaDB')
BEGIN
    ALTER DATABASE BibliotecaDB SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE BibliotecaDB;
END
GO


CREATE DATABASE BibliotecaDB;
GO

USE BibliotecaDB;
GO


CREATE TABLE Tema (
    nombre_tema VARCHAR(100) PRIMARY KEY ,
    descripcion VARCHAR(255) 
);

CREATE TABLE Usuarios (
    contrasena VARCHAR(255) NOT NULL,
    email VARCHAR(100) PRIMARY KEY,
    nombre VARCHAR(50),
	apellidos VARCHAR(50),
    tipo VARCHAR(20) CHECK (tipo IN ('Estudiante', 'Bibliotecario', 'Admin')) 
);


CREATE TABLE Estudiantes (
    email VARCHAR(100) PRIMARY KEY,
    num_prestamos INT DEFAULT 0,
    num_reservas INT DEFAULT 0,
	sanciones INT DEFAULT 0,
    FOREIGN KEY (email) REFERENCES Usuarios(email) ON DELETE CASCADE
);



CREATE TABLE Notificaciones (
    ID_notificacion INT PRIMARY KEY IDENTITY(1,1),
    mensaje TEXT NOT NULL,
    fecha_envio DATETIME DEFAULT GETDATE(),
    email VARCHAR(100) UNIQUE NOT NULL,
    FOREIGN KEY (email) REFERENCES Estudiantes(email) ON DELETE CASCADE
);

CREATE TABLE Libros (
    ISBN VARCHAR(20) PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    autor VARCHAR(100) NOT NULL,
    fecha_llegada DATE,
	num_copias INT default 1,
	disponibilidad VARCHAR(40) CHECK (disponibilidad IN ('Disponible', 'Retirado', 'Prestado', 'Reservado')),
    descripcion TEXT,
    nombre_tema VARCHAR(100),
    FOREIGN KEY (nombre_tema) REFERENCES Tema(nombre_tema)
);


CREATE TABLE Sanciones (
    ID_sancion INT PRIMARY KEY IDENTITY(1,1),
    tipo VARCHAR(100) NOT NULL,
	estado VARCHAR(40) CHECK (estado IN ('Activa', 'Cumplida')),
    fecha_inicio DATE NOT NULL,
    duracion INT,
    email VARCHAR(100) NOT NULL, 
    FOREIGN KEY (email) REFERENCES Estudiantes(email) ON DELETE CASCADE
);


CREATE TABLE Reservas (
	ID_reserva INT PRIMARY KEY IDENTITY(1,1),
	estado VARCHAR(40) CHECK (estado IN ('Pendiente', 'Cumplida')) default 'Pendiente' ,
    email VARCHAR(100) NOT NULL,
    ISBN VARCHAR(20),
    fecha_reserva DATE NOT NULL,
    FOREIGN KEY (email) REFERENCES Estudiantes(email),
    FOREIGN KEY (ISBN) REFERENCES Libros(ISBN)
);

CREATE TABLE Retirados (
    ISBN VARCHAR(20) PRIMARY KEY,
    motivo VARCHAR(300),
    fecha_retiro DATE DEFAULT GETDATE(), 
    FOREIGN KEY (ISBN) REFERENCES Libros(ISBN)
);

CREATE TABLE Prestamos (
	ID_prestamo INT PRIMARY KEY IDENTITY(1,1),
    email VARCHAR(100) NOT NULL,
    ISBN VARCHAR(20),
	estado VARCHAR(40) CHECK (estado IN ('Activo', 'Devuelto', 'Vencido')) DEFAULT 'Activo',
    fecha_prestamo DATE NOT NULL,
    fecha_devolucion DATE NOT NULL,
	prorroga BIT default 0,
    FOREIGN KEY (email) REFERENCES Estudiantes(email),
    FOREIGN KEY (ISBN) REFERENCES Libros(ISBN)
);
GO

ALTER TABLE Prestamos 
ADD CONSTRAINT DF_fecha_prestamo DEFAULT GETDATE() FOR fecha_prestamo;

ALTER TABLE Prestamos 
ADD CONSTRAINT DF_fecha_devolucion DEFAULT DATEADD(day, 14, GETDATE()) FOR fecha_devolucion;
GO

CREATE TRIGGER trg_VerificarVencimiento
ON Prestamos
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    IF EXISTS (
        SELECT 1 FROM inserted 
        WHERE fecha_devolucion < CAST(GETDATE() AS DATE) 
        AND estado = 'Activo'
    )
    BEGIN
        UPDATE P
        SET estado = 'Vencido'
        FROM Prestamos P
        INNER JOIN inserted i ON P.ID_prestamo = i.ID_prestamo
        WHERE P.fecha_devolucion < CAST(GETDATE() AS DATE)
          AND P.estado = 'Activo';
    END
END;
GO





USE BibliotecaDB;
GO



INSERT INTO Tema (nombre_tema, descripcion) VALUES 
('Matemáticas', 'Análisis matemático, álgebra, estadística y lógica pura'),
('Física', 'Estudio de la materia, energía, termodinámica y mecánica'),
('Química', 'Química orgánica, inorgánica, bioquímica y elementos químicos'),
('Biología', 'Estudio de los seres vivos, genética, evolución y ecología'),
('Geología', 'Ciencias de la Tierra, mineralogía, tectónica y paleontología'),
('Medicina', 'Ciencias de la salud, anatomía clínica, patología y farmacología'),
('Enfermería', 'Protocolos de cuidado, atención al paciente y técnicas sanitarias'),
('Veterinaria', 'Medicina animal, salud pública veterinaria y cuidado de especies'),
('Psicología', 'Comportamiento humano, procesos cognitivos y terapias'),
('Dibujo técnico', 'Geometría descriptiva, representación gráfica y sistemas de planos'),
('IA', 'Inteligencia artificial, aprendizaje automático y redes neuronales'),
('Informática', 'Algoritmia, lenguajes de programación y sistemas operativos'),
('Economía', 'Análisis micro y macroeconómico, finanzas y contabilidad'),
('Historia', 'Investigación histórica, cronología y análisis de eventos pasados'),
('Filosofía', 'Ética, metafísica, teoría del conocimiento y pensamiento crítico'),
('Derecho', 'Sistemas jurídicos, leyes civiles, penales y jurisprudencia'),
('Literatura', 'Obras clásicas, narrativa, poesía y análisis literario'),
('Música', 'Teoría musical, solfeo, composición e historia de la música'),
('Arte', 'Historia del arte, teoría estética, pintura, escultura y diseño'),
('Electrónica', 'Circuitos eléctricos, sistemas de control y microelectrónica'),
('Mecánica', 'Diseño de máquinas, termodinámica aplicada y cinemática'),
('Diseño', 'Diseño gráfico, industrial, de interiores y metodologías creativas'),
('Deporte', 'Ciencias del deporte, fisiología del ejercicio y metodología de entrenamiento');


INSERT INTO Usuarios (contrasena, email, nombre, apellidos, tipo) VALUES 
('1234', '1234', 'Elena', 'Rodríguez Martínez', 'Estudiante'),
('123', '123', 'Miguel', 'Gómez Pérez', 'Estudiante'),
('pass_ing', 'smartm00@estudiantes.unileon.es', 'Sara', 'Martín Morales', 'Estudiante'),
('pass_eco', 'dferns00@estudiantes.unileon.es', 'David', 'Fernández Silva', 'Estudiante'),
('pass_arq', 'ldiazf00@estudiantes.unileon.es', 'Laura', 'Díaz Ferrer', 'Estudiante'),
('pass_bio', 'sblang00@estudiantes.unileon.es', 'Sergio', 'Blanco García', 'Estudiante'),
('pass_vet', 'lruizm00@estudiantes.unileon.es', 'Lucía', 'Ruiz Méndez', 'Estudiante'),
('pass_der', 'pcanol00@estudiantes.unileon.es', 'Pablo', 'Cano López', 'Estudiante'),
('pass_fil', 'amends00@estudiantes.unileon.es', 'Ana', 'Méndez Sánchez', 'Estudiante'),
('pass_inf', 'jvazqh00@estudiantes.unileon.es', 'Javier', 'Vázquez Hernández', 'Estudiante'),
('pass_ext', 'sblang01@estudiantes.unileon.es', 'Sandra', 'Blanco Gómez', 'Estudiante'),

('biblio_jefe', 'carlos.biblio@unileon.es', 'Carlos', 'López', 'Bibliotecario'),
('biblio_tarde', 'marta.biblio@unileon.es', 'Marta', 'Sánchez', 'Bibliotecario'),
('12', '12', 'Pepe', 'Pepín', 'Bibliotecario'),

('admin_root', 'sistemas.biblioteca@unileon.es', 'Admin', 'Sistemas IT', 'Admin'),
('1', 'admin2.biblioteca@unileon.es', 'Admin2', 'Sistemas IT2', 'Admin');


INSERT INTO Estudiantes (email, num_prestamos, num_reservas, sanciones)
SELECT email, 0, 0, 0 
FROM Usuarios 
WHERE tipo = 'Estudiante';


INSERT INTO Libros (ISBN, titulo, autor, fecha_llegada, num_copias, disponibilidad, descripcion, nombre_tema) VALUES 
('978-84-MAT01', 'Cálculo Infinitesimal', 'Michael Spivak', '2024-01-15', 1, 'Disponible', 'Texto fundamental de análisis matemático para ingenierías.', 'Matemáticas'),

('978-84-IA02', 'Inteligencia Artificial: Un Enfoque Moderno', 'Stuart Russell', '2025-05-10', 1, 'Disponible', 'El estándar mundial en enseñanza de IA y agentes inteligentes.', 'IA'),

('978-84-FIS03', 'Física para la ciencia y la tecnología', 'Paul A. Tipler', '2024-02-20', 1, 'Disponible', 'Volumen 1: Mecánica, oscilaciones y ondas, termodinámica.', 'Física'),

('978-84-MED04', 'Anatomía de Gray', 'Henry Gray', '2023-09-01', 1, 'Retirado', 'Edición de colección. Solo consulta en sala de investigadores.', 'Medicina'),

('978-84-INF05', 'Clean Code: A Handbook of Agile Software Craftsmanship', 'Robert C. Martin', '2024-10-15', 1, 'Disponible', 'Mejores prácticas para desarrollo de software profesional.', 'Informática'),

('978-84-DER06', 'Teoría Pura del Derecho', 'Hans Kelsen', '2023-11-20', 1, 'Disponible', 'Obra clásica de la filosofía del derecho y positivismo.', 'Derecho'),

('978-84-LIT07', 'Cien años de soledad', 'Gabriel García Márquez', '2022-03-20', 1, 'Disponible', 'Obra cumbre del realismo mágico y la literatura hispana.', 'Literatura'),

('978-84-PSI08', 'Psicología Social', 'David G. Myers', '2025-01-05', 1, 'Disponible', 'Estudio científico de cómo las personas piensan unas de otras.', 'Psicología'),

('978-84-HIS09', 'Sapiens: De animales a dioses', 'Yuval Noah Harari', '2024-08-12', 1, 'Disponible', 'Una breve historia de la evolución de la humanidad.', 'Historia'),

('978-84-MUS10', 'Teoría Completa de la Música', 'Dionisio de Pedro', '2023-04-14', 1, 'Disponible', 'Manual técnico avanzado de solfeo, armonía y composición.', 'Música');




INSERT INTO Prestamos (email, ISBN)
VALUES 
('estudiante1@estudiantes.unileon.es', '978-84-IA02'),
('sara.martin@estudiantes.unileon.es', '978-84-PSI08');


USE BibliotecaDB;
CREATE USER biblioteca_user FOR LOGIN biblioteca_user;
ALTER ROLE db_owner ADD MEMBER biblioteca_user;
ALTER LOGIN biblioteca_user WITH PASSWORD = 'pruebaISD2024';
ALTER LOGIN biblioteca_user ENABLE;
