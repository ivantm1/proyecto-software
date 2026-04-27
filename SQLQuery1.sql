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

('1234', 'estudiante1@estudiantes.unileon.es', 'Elena', 'Rodr�guez', 'Estudiante'),
('123', '123', 'Miguel', 'G�mez', 'Estudiante'),
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


USE BibliotecaDB;
CREATE USER biblioteca_user FOR LOGIN biblioteca_user;
ALTER ROLE db_owner ADD MEMBER biblioteca_user;
ALTER LOGIN biblioteca_user WITH PASSWORD = 'pruebaISD2024';
ALTER LOGIN biblioteca_user ENABLE;


INSERT INTO Libros (ISBN, titulo, autor, fecha_llegada, num_copias, disponibilidad, descripcion, nombre_tema) VALUES 
('978-84-MAT01', 'Cálculo Infinitesimal', 'Michael Spivak', '2024-01-15', 5, 'Disponible', 'Texto fundamental de análisis matemático para ingenierías.', 'Matemáticas'),

('978-84-IA02', 'Inteligencia Artificial: Un Enfoque Moderno', 'Stuart Russell', '2025-05-10', 3, 'Prestado', 'El estándar mundial en enseñanza de IA y agentes inteligentes.', 'IA'),

('978-84-FIS03', 'Física para la ciencia y la tecnología', 'Paul A. Tipler', '2024-02-20', 4, 'Disponible', 'Volumen 1: Mecánica, oscilaciones y ondas, termodinámica.', 'Física'),

('978-84-MED04', 'Anatomía de Gray', 'Henry Gray', '2023-09-01', 2, 'Retirado', 'Edición de colección. Solo consulta en sala de investigadores.', 'Medicina'),

('978-84-INF05', 'Clean Code: A Handbook of Agile Software Craftsmanship', 'Robert C. Martin', '2024-10-15', 8, 'Disponible', 'Mejores prácticas para desarrollo de software profesional.', 'Informática'),

('978-84-DER06', 'Teoría Pura del Derecho', 'Hans Kelsen', '2023-11-20', 1, 'Disponible', 'Obra clásica de la filosofía del derecho y positivismo.', 'Derecho'),

('978-84-LIT07', 'Cien años de soledad', 'Gabriel García Márquez', '2022-03-20', 10, 'Disponible', 'Obra cumbre del realismo mágico y la literatura hispana.', 'Literatura'),

('978-84-PSI08', 'Psicología Social', 'David G. Myers', '2025-01-05', 6, 'Prestado', 'Estudio científico de cómo las personas piensan unas de otras.', 'Psicología'),

('978-84-HIS09', 'Sapiens: De animales a dioses', 'Yuval Noah Harari', '2024-08-12', 4, 'Disponible', 'Una breve historia de la evolución de la humanidad.', 'Historia'),

('978-84-MUS10', 'Teoría Completa de la Música', 'Dionisio de Pedro', '2023-04-14', 7, 'Disponible', 'Manual técnico avanzado de solfeo, armonía y composición.', 'Música');

GO

