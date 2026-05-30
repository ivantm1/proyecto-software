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




CREATE TABLE Libros (
    ISBN VARCHAR(20) PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    autor VARCHAR(100) NOT NULL,
    fecha_llegada DATE DEFAULT GETDATE(),
	num_copias INT default 1,
	disponibilidad VARCHAR(40) CHECK (disponibilidad IN ('Disponible', 'Retirado', 'Prestado', 'Reservado')) default 'Disponible',
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
('1', '1', 'Admin2', 'Sistemas IT2', 'Admin');


INSERT INTO Estudiantes (email, num_prestamos, num_reservas, sanciones)
SELECT email, 0, 0, 0 
FROM Usuarios 
WHERE tipo = 'Estudiante';


INSERT INTO Libros (ISBN, titulo, autor, descripcion, nombre_tema) VALUES 

-- Matemáticas
('978-84-291-5032-2', 'Cálculo Diferencial e Integral', 'N. Piskunov', 'Cálculo clásico en una y varias variables con abundantes ejercicios resueltos.', 'Matemáticas'),
('978-84-7615-402-7', 'Matemáticas Discretas y sus Aplicaciones', 'Kenneth H. Rosen', 'Lógica, grafos, combinatoria y teoría de números para informáticos.', 'Matemáticas'),
('978-84-8322-910-6', 'Probabilidad y Estadística para Ingeniería', 'Jay L. Devore', 'Distribuciones de probabilidad, inferencia estadística y regresión aplicada.', 'Matemáticas'),
 
-- Física
('978-84-291-4198-6', 'Mecánica Clásica', 'Herbert Goldstein', 'Formulaciones lagrangiana y hamiltoniana de la mecánica clásica avanzada.', 'Física'),
('978-84-9835-320-8', 'Óptica', 'Eugene Hecht', 'Naturaleza de la luz, interferencia, difracción y óptica moderna.', 'Física'),
('978-84-7615-561-1', 'Termodinámica y Mecánica Estadística', 'Frederick Reif', 'Fundamentos estadísticos de la termodinámica y los sistemas en equilibrio.', 'Física'),
 
-- Química
('978-84-291-4310-2', 'Fisicoquímica', 'Peter Atkins', 'Termodinámica química, cinética y mecánica cuántica aplicada a la química.', 'Química'),
('978-84-9732-614-3', 'Química Analítica Cuantitativa', 'Daniel C. Harris', 'Técnicas analíticas: volumetría, espectroscopía y cromatografía.', 'Química'),
 
-- Biología
('978-84-291-7842-6', 'Ecología', 'Eugene P. Odum', 'Fundamentos de ecología: ecosistemas, ciclos biogeoquímicos y biodiversidad.', 'Biología'),
('978-84-8322-337-1', 'Microbiología', 'Michael T. Madigan', 'Estructura, metabolismo y genética de microorganismos procariotas y eucariotas.', 'Biología'),
('978-84-9835-067-2', 'Fisiología Vegetal', 'Lincoln Taiz', 'Procesos fisiológicos de las plantas: nutrición, fotosíntesis y desarrollo.', 'Biología'),
 
-- Geología
('978-84-7615-318-1', 'Petrología Ígnea y Metamórfica', 'Myron G. Best', 'Origen, clasificación y distribución de rocas ígneas y metamórficas.', 'Geología'),
('978-84-291-6508-1', 'Geomorfología', 'Andrew Goudie', 'Formas del relieve terrestre y los procesos que las originan y modifican.', 'Geología'),
 
-- Medicina
('978-84-9835-780-0', 'Patología Estructural y Funcional', 'Vinay Kumar', 'Bases celulares y moleculares de las enfermedades humanas más relevantes.', 'Medicina'),
('978-84-7615-940-4', 'Tratado de Fisiología Médica', 'Arthur C. Guyton', 'Funcionamiento del cuerpo humano a nivel de órganos y sistemas.', 'Medicina'),
('978-84-291-5560-0', 'Urgencias en Medicina', 'Peter Rosen', 'Diagnóstico y manejo de situaciones de urgencia en el entorno hospitalario.', 'Medicina'),
 
-- Enfermería
('978-84-9835-102-0', 'Enfermería Médico-Quirúrgica', 'Donna D. Ignatavicius', 'Cuidados de enfermería en patología médica y quirúrgica del adulto.', 'Enfermería'),
('978-84-7615-875-9', 'Farmacología en Enfermería', 'Richard A. Lehne', 'Fundamentos farmacológicos para la práctica enfermera segura.', 'Enfermería'),
 
-- Veterinaria
('978-84-291-8201-0', 'Atlas de Anatomía Veterinaria', 'Klaus-Dieter Budras', 'Anatomía comparada de animales domésticos con ilustraciones detalladas.', 'Veterinaria'),
('978-84-9735-512-5', 'Microbiología Veterinaria', 'Ernst L. Biberstein', 'Agentes infecciosos bacterianos, víricos y micóticos en animales.', 'Veterinaria'),
 
-- Psicología
('978-84-291-2450-7', 'Psicopatología General', 'Karl Jaspers', 'Descripción y clasificación de los fenómenos psicopatológicos fundamentales.', 'Psicología'),
('978-84-8322-512-2', 'Neurociencia y Conducta', 'Eric R. Kandel', 'Bases neurobiológicas del comportamiento humano normal y patológico.', 'Psicología'),
('978-84-9835-230-4', 'Psicología del Desarrollo', 'Laura E. Berk', 'Desarrollo humano desde la concepción hasta la vejez: teorías y evidencia.', 'Psicología'),
 
-- Informática
('978-84-9735-730-3', 'Redes de Computadores', 'Andrew S. Tanenbaum', 'Protocolos de red, modelo TCP/IP y tecnologías de comunicación de datos.', 'Informática'),
('978-84-7615-689-2', 'Bases de Datos: Diseño y Gestión', 'Ramon A. Mata-Toledo', 'Modelado relacional, SQL, normalización y administración de bases de datos.', 'Informática'),
('978-84-8322-855-0', 'Ingeniería del Software', 'Roger S. Pressman', 'Procesos, métodos y herramientas para el desarrollo profesional de software.', 'Informática'),
('978-84-291-6003-1', 'Compiladores: Principios, Técnicas y Herramientas', 'Alfred V. Aho', 'Análisis léxico, sintáctico y semántico y generación de código.', 'Informática'),
 
-- IA
('978-84-9835-944-6', 'Visión por Computador', 'Richard Szeliski', 'Procesamiento de imagen, detección de objetos y reconocimiento visual.', 'IA'),
('978-84-7615-771-4', 'Procesamiento del Lenguaje Natural', 'Daniel Jurafsky', 'Modelos lingüísticos, análisis sintáctico y sistemas de diálogo.', 'IA'),
 
-- Economía
('978-84-291-3587-2', 'Microeconomía Intermedia', 'Hal R. Varian', 'Teoría del consumidor, producción, mercados y equilibrio general.', 'Economía'),
('978-84-9732-920-5', 'Contabilidad Financiera', 'Juan García Moreno', 'Plan General Contable español, registro y análisis de estados financieros.', 'Economía'),
 
-- Historia
('978-84-7615-295-5', 'La Revolución Francesa', 'Albert Soboul', 'Causas, desarrollo y consecuencias de la Revolución Francesa 1789-1799.', 'Historia'),
('978-84-291-3012-6', 'Historia de la Ciencia', 'Stephen F. Mason', 'Evolución del pensamiento científico desde la Antigüedad hasta el siglo XX.', 'Historia'),
('978-84-9835-601-8', 'Historia Medieval de España', 'José Ángel García de Cortázar', 'Reinos medievales ibéricos: visigodos, Al-Ándalus y la Reconquista.', 'Historia'),
 
-- Filosofía
('978-84-291-1720-2', 'La República', 'Platón', 'El Estado ideal, la justicia y la educación según el pensamiento platónico.', 'Filosofía'),
('978-84-8322-240-4', 'Ética a Nicómaco', 'Aristóteles', 'Fundamentos de la ética aristotélica: virtud, felicidad y vida buena.', 'Filosofía'),
 
-- Derecho
('978-84-291-6908-5', 'Derecho Constitucional Español', 'Luis López Guerra', 'La Constitución de 1978: derechos fundamentales y organización del Estado.', 'Derecho'),
('978-84-9835-843-2', 'Derecho Mercantil', 'Rodrigo Uría', 'Empresa, sociedades mercantiles, títulos valores y contratos comerciales.', 'Derecho'),
 
-- Literatura
('978-84-376-0812-9', 'La Casa de Bernarda Alba', 'Federico García Lorca', 'Drama sobre la represión, el honor y la condición femenina en la España rural.', 'Literatura'),
('978-84-9732-430-9', 'Niebla', 'Miguel de Unamuno', 'Novela existencialista sobre la ficción, la conciencia y el libre albedrío.', 'Literatura'),
('978-84-291-4690-5', 'El Quijote de la Mancha: Análisis Literario', 'Martín de Riquer', 'Estudio crítico y contexto histórico de la obra de Cervantes.', 'Literatura'),
 
-- Música
('978-84-9835-310-9', 'Armonía', 'Walter Piston', 'Tratado completo de armonía tonal: acordes, modulación y análisis armónico.', 'Música'),
('978-84-7615-540-6', 'El Sistema Tonal', 'Carl Dahlhaus', 'Evolución histórica y fundamentos teóricos del sistema tonal occidental.', 'Música'),
 
-- Arte
('978-84-291-3340-0', 'El Arte del Siglo XX', 'Ingo F. Walther', 'Movimientos artísticos del siglo XX: impresionismo, cubismo y arte abstracto.', 'Arte'),
('978-84-9732-567-2', 'Historia de la Arquitectura', 'Spiro Kostof', 'Evolución de la arquitectura mundial desde los primeros asentamientos.', 'Arte'),
 
-- Electrónica
('978-84-291-5234-0', 'Sistemas de Control Automático', 'Benjamin C. Kuo', 'Diseño y análisis de sistemas de control en tiempo continuo y discreto.', 'Electrónica'),
('978-84-9835-670-4', 'Comunicaciones Analógicas y Digitales', 'Simon Haykin', 'Modulación, codificación y transmisión de señales en sistemas de comunicación.', 'Electrónica'),
 
-- Mecánica
('978-84-291-7012-3', 'Resistencia de Materiales', 'Ferdinand P. Beer', 'Tensiones, deformaciones y diseño de elementos estructurales y mecánicos.', 'Mecánica'),
('978-84-8322-745-4', 'Mecánica de Fluidos', 'Frank M. White', 'Estática y dinámica de fluidos, flujo interno y externo, y turbomaquinaria.', 'Mecánica'),
 
-- Diseño
('978-84-9835-098-6', 'Fundamentos del Diseño Industrial', 'Mike Baxter', 'Metodología del diseño de productos: usuario, ergonomía y prototipado.', 'Diseño'),
 
-- Deporte
('978-84-7615-350-1', 'Fisiología del Esfuerzo y del Deporte', 'Jack H. Wilmore', 'Respuestas fisiológicas al ejercicio y adaptaciones al entrenamiento.', 'Deporte'),
('978-84-9835-421-2', 'Teoría y Práctica del Entrenamiento Deportivo', 'Tudor O. Bompa', 'Principios del entrenamiento: periodización, cargas y planificación.', 'Deporte'),
 
-- Dibujo técnico
('978-84-291-6124-3', 'Dibujo Técnico Industrial', 'José M. Simón Mata', 'Normalización, vistas, cortes y acotación según normas UNE e ISO.', 'Dibujo técnico'),
('978-84-8322-388-3', 'Geometría Descriptiva', 'José Izquierdo Asensi', 'Sistema diédrico, acotado y cónico para la representación gráfica técnica.', 'Dibujo técnico'),

-- Matemáticas
('978-84-291-5015-5', 'Análisis Matemático Vol. 1', 'Tom M. Apostol', 'Cálculo diferencial e integral en una variable con rigor matemático.', 'Matemáticas'),
('978-84-9732-052-3', 'Álgebra Lineal', 'Serge Lang', 'Introducción al álgebra lineal con espacios vectoriales y transformaciones lineales.', 'Matemáticas'),
('978-84-7615-316-7', 'Estadística para Administración y Economía', 'Richard I. Levin', 'Métodos estadísticos aplicados a la toma de decisiones empresariales.', 'Matemáticas'),

-- Física
('978-84-291-4025-5', 'Física Universitaria Vol. 1', 'Hugh D. Young', 'Mecánica, termodinámica y ondas para estudiantes de ingeniería y ciencias.', 'Física'),
('978-84-8322-932-8', 'Conceptos de Física Moderna', 'Arthur Beiser', 'Relatividad, mecánica cuántica, física nuclear y partículas subatómicas.', 'Física'),
('978-84-291-5414-6', 'Electricidad y Magnetismo', 'Edward M. Purcell', 'Fundamentos del electromagnetismo con enfoque en intuición física.', 'Física'),

-- Química
('978-84-291-4002-6', 'Química General', 'Linus Pauling', 'Principios de química general: estructura atómica, enlace y reactividad.', 'Química'),
('978-84-9732-284-8', 'Química Orgánica', 'Paula Y. Bruice', 'Reacciones, mecanismos y síntesis de compuestos orgánicos.', 'Química'),
('978-84-7615-898-8', 'Bioquímica', 'Jeremy M. Berg', 'Estructura y función de biomoléculas, metabolismo y regulación celular.', 'Química'),

-- Biología
('978-84-291-7630-9', 'Biología Celular y Molecular', 'James D. Watson', 'Genética molecular, expresión génica y biología celular moderna.', 'Biología'),
('978-84-9732-501-6', 'El Origen de las Especies', 'Charles Darwin', 'Obra fundacional de la teoría de la evolución por selección natural.', 'Biología'),
('978-84-8322-455-2', 'Genética', 'Benjamin A. Pierce', 'Principios de herencia, genética molecular y genómica.', 'Biología'),

-- Geología
('978-84-291-6312-4', 'Geología Física', 'Brian J. Skinner', 'Procesos geológicos internos y externos que modelan la superficie terrestre.', 'Geología'),
('978-84-7615-204-7', 'Mineralogía Determinativa', 'Cornelius S. Hurlbut', 'Identificación y clasificación de minerales por propiedades físicas y químicas.', 'Geología'),

-- Medicina
('978-84-9835-203-4', 'Anatomía Humana', 'Frank H. Netter', 'Atlas completo de anatomía humana con ilustraciones detalladas por sistemas.', 'Medicina'),
('978-84-291-3985-3', 'Harrison: Principios de Medicina Interna', 'J. Larry Jameson', 'Referencia clínica estándar en medicina interna y diagnóstico diferencial.', 'Medicina'),
('978-84-9835-612-4', 'Farmacología Básica y Clínica', 'Bertram G. Katzung', 'Mecanismos de acción farmacológica, farmacocinética y usos terapéuticos.', 'Medicina'),

-- Enfermería
('978-84-7615-993-0', 'Fundamentos de Enfermería', 'Patricia A. Potter', 'Principios y habilidades fundamentales de la práctica enfermera.', 'Enfermería'),
('978-84-9835-445-8', 'Diagnósticos Enfermeros: Definiciones y Clasificación', 'NANDA International', 'Taxonomía oficial de diagnósticos de enfermería para la práctica clínica.', 'Enfermería'),

-- Veterinaria
('978-84-291-8034-4', 'Medicina y Cirugía del Caballo', 'Timothy S. Mair', 'Diagnóstico y tratamiento de enfermedades en équidos.', 'Veterinaria'),
('978-84-9735-401-2', 'Medicina Interna Veterinaria', 'Stephen J. Ettinger', 'Enfermedades internas de pequeños animales: diagnóstico y terapéutica.', 'Veterinaria'),

-- Psicología
('978-84-291-2210-7', 'Psicología', 'David G. Myers', 'Introducción completa a la psicología científica y sus principales corrientes.', 'Psicología'),
('978-84-7615-742-4', 'El Hombre en Busca de Sentido', 'Viktor E. Frankl', 'Logoterapia y experiencias en los campos de concentración nazis.', 'Psicología'),
('978-84-9835-178-5', 'Psicología Cognitiva', 'Robert J. Sternberg', 'Procesos mentales superiores: atención, memoria, razonamiento y lenguaje.', 'Psicología'),

-- Informática
('978-84-7615-544-4', 'Introducción a los Algoritmos', 'Thomas H. Cormen', 'Análisis y diseño de algoritmos con demostraciones formales.', 'Informática'),
('978-84-8322-783-6', 'El Lenguaje de Programación C', 'Brian W. Kernighan', 'Guía definitiva del lenguaje C escrita por sus creadores.', 'Informática'),
('978-84-9735-610-8', 'Sistemas Operativos Modernos', 'Andrew S. Tanenbaum', 'Diseño e implementación de sistemas operativos: procesos, memoria y E/S.', 'Informática'),
('978-84-291-5788-8', 'Estructura de Computadores', 'David A. Patterson', 'Arquitectura de computadores, conjunto de instrucciones y jerarquía de memoria.', 'Informática'),

-- IA
('978-84-9835-821-0', 'Inteligencia Artificial: Un Enfoque Moderno', 'Stuart Russell', 'Fundamentos de IA: búsqueda, aprendizaje, razonamiento y planificación.', 'IA'),
('978-84-7615-906-0', 'Deep Learning', 'Ian Goodfellow', 'Redes neuronales profundas: fundamentos matemáticos y aplicaciones prácticas.', 'IA'),
('978-84-8322-340-1', 'Aprendizaje Automático', 'Tom M. Mitchell', 'Algoritmos de machine learning: supervisado, no supervisado y por refuerzo.', 'IA'),

-- Economía
('978-84-291-3321-9', 'Principios de Economía', 'N. Gregory Mankiw', 'Microeconomía y macroeconomía para estudiantes universitarios de primer año.', 'Economía'),
('978-84-9735-230-8', 'El Capital', 'Karl Marx', 'Análisis crítico del capitalismo, plusvalía y relaciones de producción.', 'Economía'),
('978-84-7615-667-0', 'Macroeconomía', 'Olivier Blanchard', 'Modelos macroeconómicos: PIB, inflación, desempleo y política fiscal.', 'Economía'),

-- Historia
('978-84-291-2987-8', 'Historia Universal Contemporánea', 'Eric Hobsbawm', 'Análisis del siglo XX: guerras, revoluciones y transformaciones sociales.', 'Historia'),
('978-84-9835-053-5', 'Sapiens: De Animales a Dioses', 'Yuval Noah Harari', 'Historia breve de la humanidad desde el Homo sapiens hasta la modernidad.', 'Historia'),
('978-84-7615-480-5', 'Historia de España', 'José Luis Martín', 'Evolución histórica de la Península Ibérica desde la Antigüedad.', 'Historia'),

-- Filosofía
('978-84-291-1456-0', 'Crítica de la Razón Pura', 'Immanuel Kant', 'Fundamentos del conocimiento humano y los límites de la razón.', 'Filosofía'),
('978-84-9835-394-9', 'El Mundo como Voluntad y Representación', 'Arthur Schopenhauer', 'Metafísica de la voluntad y la representación como principios del mundo.', 'Filosofía'),
('978-84-7615-112-5', 'Meditaciones Metafísicas', 'René Descartes', 'Fundamentos del pensamiento racionalista y la duda metódica cartesiana.', 'Filosofía'),

-- Derecho
('978-84-291-6732-0', 'Derecho Penal: Parte General', 'Francisco Muñoz Conde', 'Fundamentos del derecho penal, teoría del delito y consecuencias jurídicas.', 'Derecho'),
('978-84-9835-712-1', 'Instituciones de Derecho Civil', 'Federico de Castro', 'Obligaciones, contratos y derechos reales en el derecho civil español.', 'Derecho'),

-- Literatura
('978-84-376-0494-7', 'Don Quijote de la Mancha', 'Miguel de Cervantes', 'La obra cumbre de la literatura española y una de las primeras novelas modernas.', 'Literatura'),
('978-84-9732-788-1', 'Cien Años de Soledad', 'Gabriel García Márquez', 'Saga de la familia Buendía en el mítico Macondo, obra maestra del realismo mágico.', 'Literatura'),
('978-84-291-4456-7', 'La Metamorfosis', 'Franz Kafka', 'Relato de la transformación de Gregor Samsa y la alienación del individuo moderno.', 'Literatura'),

-- Música
('978-84-8322-601-3', 'Teoría de la Música', 'Enrique Nebreda', 'Fundamentos de teoría musical: solfeo, armonía y contrapunto.', 'Música'),
('978-84-9735-089-2', 'Historia de la Música Occidental', 'Donald J. Grout', 'Evolución de la música clásica occidental desde la Edad Media hasta el siglo XX.', 'Música'),

-- Arte
('978-84-291-3104-8', 'Historia del Arte', 'Ernst H. Gombrich', 'Recorrido por el arte occidental desde las cavernas hasta el arte contemporáneo.', 'Arte'),
('978-84-7615-823-0', 'El Arte de Ver', 'John Berger', 'Análisis crítico de la imagen, la pintura y la fotografía en la cultura occidental.', 'Arte'),

-- Electrónica
('978-84-9835-541-7', 'Electrónica: Teoría de Circuitos', 'Robert L. Boylestad', 'Análisis de circuitos eléctricos y electrónicos en corriente continua y alterna.', 'Electrónica'),
('978-84-291-5901-1', 'Microelectrónica', 'Behzad Razavi', 'Diseño de circuitos integrados analógicos y digitales en tecnología CMOS.', 'Electrónica'),

-- Diseño
('978-84-9835-230-0', 'Diseño Gráfico: Principios y Práctica', 'David Dabner', 'Fundamentos del diseño gráfico: tipografía, color, composición y maquetación.', 'Diseño');






USE BibliotecaDB;
CREATE USER biblioteca_user FOR LOGIN biblioteca_user;
ALTER ROLE db_owner ADD MEMBER biblioteca_user;
ALTER LOGIN biblioteca_user WITH PASSWORD = 'pruebaISD2024';
ALTER LOGIN biblioteca_user ENABLE;
