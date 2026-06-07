USE BibliotecaDB;
GO

/* Cleanup: re-runnable script - remove previous test data */
DELETE FROM Prestamos WHERE email LIKE 'test_%';
DELETE FROM Reservas WHERE email LIKE 'test_%';
DELETE FROM Sanciones WHERE email LIKE 'test_%';
DELETE FROM Retirados WHERE ISBN IN (
    '978-84-291-5032-2', '978-84-7615-402-7', '978-84-9735-730-3', '978-84-7615-689-2', '978-84-9735-610-8', '978-84-291-4025-5', '978-84-291-6124-3'
);
DELETE FROM Estudiantes WHERE email LIKE 'test_%';
DELETE FROM Usuarios WHERE email LIKE 'test_%';

-- Reset influenced books to a neutral availability so script can run repeatedly
UPDATE Libros SET disponibilidad = 'Disponible' WHERE ISBN IN (
    '978-84-291-5032-2', '978-84-7615-402-7', '978-84-9735-730-3', '978-84-7615-689-2', '978-84-9735-610-8', '978-84-291-4025-5', '978-84-291-6124-3'
);
GO

/* 1. Create test users (prefixed with test_) and corresponding Estudiantes */
INSERT INTO Usuarios (contrasena, email, nombre, apellidos, tipo) VALUES
('pass', 'test_user1@example.com', 'Test', 'Usuario1', 'Estudiante'),
('pass', 'test_user2@example.com', 'Test', 'Usuario2', 'Estudiante'),
('pass', 'test_user3@example.com', 'Test', 'Usuario3', 'Estudiante');

INSERT INTO Estudiantes (email, num_prestamos, num_reservas, sanciones) VALUES
('test_user1@example.com', 0, 0, 0),
('test_user2@example.com', 0, 0, 0),
('test_user3@example.com', 0, 0, 0);
GO

/* 2. Préstamos: one per requested state */

-- 2.1 Activo (no prórroga)
UPDATE Libros SET disponibilidad = 'Prestado' WHERE ISBN = '978-84-7615-402-7';
INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga)
VALUES ('test_user1@example.com', '978-84-7615-402-7', 'Activo',
        CAST(GETDATE() AS DATE),
        CAST(DATEADD(day, 14, GETDATE()) AS DATE), 0);

-- 2.2 Activo + prórroga = 1 (extendida 7 días)
UPDATE Libros SET disponibilidad = 'Prestado' WHERE ISBN = '978-84-9735-730-3';
INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga)
VALUES ('test_user1@example.com', '978-84-9735-730-3', 'Activo',
        CAST(GETDATE() AS DATE),
        CAST(DATEADD(day, 21, GETDATE()) AS DATE), 1);

-- 2.3 Vencido (fecha_devolucion pasada)
UPDATE Libros SET disponibilidad = 'Prestado' WHERE ISBN = '978-84-291-5032-2';
INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga)
VALUES ('test_user2@example.com', '978-84-291-5032-2', 'Vencido',
        CAST(DATEADD(day, -30, GETDATE()) AS DATE),
        CAST(DATEADD(day, -3, GETDATE()) AS DATE), 0);

-- 2.4 Devuelto (libro ya devuelto -> disponibilidad = 'Disponible')
-- We insert a Devuelto préstamo (histórico) and ensure the libro is Disponible
INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga)
VALUES ('test_user2@example.com', '978-84-7615-689-2', 'Devuelto',
        CAST(DATEADD(day, -20, GETDATE()) AS DATE),
        CAST(DATEADD(day, -6, GETDATE()) AS DATE), 0);
UPDATE Libros SET disponibilidad = 'Disponible' WHERE ISBN = '978-84-7615-689-2';
GO

/* 3. Reservas: Espera (recién creada), Espera lista para recoger (Recoger), Caducada */

-- 3.1 Reserva 'Espera' recién creada: the book remains 'Prestado' (not reserved yet)
-- Use the same ISBN that is currently prestado ('978-84-7615-402-7')
INSERT INTO Reservas (estado, email, ISBN, fecha_reserva)
VALUES ('Espera', 'test_user3@example.com', '978-84-7615-402-7', CAST(GETDATE() AS DATE));
-- Do NOT change disponibilidad: it remains 'Prestado'

-- 3.2 Reserva lista para recoger -> estado 'Recoger' and set book 'Reservado'
UPDATE Libros SET disponibilidad = 'Reservado' WHERE ISBN = '978-84-9735-610-8';
INSERT INTO Reservas (estado, email, ISBN, fecha_reserva)
VALUES ('Recoger', 'test_user3@example.com', '978-84-9735-610-8', CAST(DATEADD(day, -2, GETDATE()) AS DATE));

-- 3.3 Reserva Caducada -> student didn't pick up within 7 days, book back to 'Disponible'
INSERT INTO Reservas (estado, email, ISBN, fecha_reserva)
VALUES ('Caducada', 'test_user3@example.com', '978-84-291-4025-5', CAST(DATEADD(day, -20, GETDATE()) AS DATE));
-- Mantener como 'Reservado' en catálogo aunque la reserva haya caducado (solicitud del equipo)
UPDATE Libros SET disponibilidad = 'Reservado' WHERE ISBN = '978-84-291-4025-5';
GO

/* 4. Sanciones: Activa, Pendiente, Cumplida */
-- 4.1 Activa
INSERT INTO Sanciones (tipo, estado, fecha_inicio, duracion, email)
VALUES ('Retraso', 'Activa', CAST(GETDATE() AS DATE), 30, 'test_user1@example.com');

-- 4.2 Pendiente (queued because an Activa exists for same student in normal logic)
INSERT INTO Sanciones (tipo, estado, fecha_inicio, duracion, email)
VALUES ('Comportamiento', 'Pendiente', CAST(DATEADD(day, 1, GETDATE()) AS DATE), 14, 'test_user1@example.com');

-- 4.3 Cumplida (historical)
INSERT INTO Sanciones (tipo, estado, fecha_inicio, duracion, email)
VALUES ('Multa', 'Cumplida', CAST(DATEADD(day, -60, GETDATE()) AS DATE), 15, 'test_user2@example.com');
GO

/* 5. Retirados: example of a withdrawn book */
UPDATE Libros SET disponibilidad = 'Retirado' WHERE ISBN = '978-84-291-6124-3';
INSERT INTO Retirados (ISBN, motivo, fecha_retiro)
VALUES ('978-84-291-6124-3', 'Colección desactualizada', CAST(GETDATE() AS DATE));
GO

/* Verification queries: counts grouped by (tabla, estado) for test data */
SELECT 'Prestamos' AS tabla, estado, COUNT(*) AS cnt
FROM Prestamos
WHERE email LIKE 'test_%'
GROUP BY estado

UNION ALL

SELECT 'Reservas' AS tabla, estado, COUNT(*) AS cnt
FROM Reservas
WHERE email LIKE 'test_%'
GROUP BY estado

UNION ALL

SELECT 'Sanciones' AS tabla, estado, COUNT(*) AS cnt
FROM Sanciones
WHERE email LIKE 'test_%'
GROUP BY estado;
GO

/* -------------------------------------------------- */
/* Ejemplos adicionales de Reservas para cuentas '123' */
/* Muestran comprobaciones: límite de 3 reservas, una reserva activa por ISBN, y cambios de estado */
/* Usamos los usuarios existentes en DataBase.sql con email = '123' y '1234' */

-- Asegurarnos de que los usuarios existen como Estudiantes (ya presentes en DataBase.sql)
-- (si no existen, crearíamos filas similares a las de test_ )

/* Escenario 1: usuario '123' intenta reservar varios libros (hasta 3 permitidas) */
-- Marcar 3 libros como Prestado para permitir reservas en Espera
UPDATE Libros SET disponibilidad = 'Prestado' WHERE ISBN IN ('978-84-9735-730-3','978-84-7615-689-2','978-84-8322-855-0');

DECLARE @countReservas INT;
SELECT @countReservas = COUNT(*) FROM Reservas WHERE email = '123' AND estado IN ('Espera','Recoger');

IF @countReservas < 3
BEGIN
        -- Reserva 1
        IF NOT EXISTS(SELECT 1 FROM Reservas WHERE ISBN = '978-84-9735-730-3' AND estado IN ('Espera','Recoger'))
        BEGIN
                INSERT INTO Reservas (estado, email, ISBN, fecha_reserva)
                VALUES ('Espera', '123', '978-84-9735-730-3', CAST(GETDATE() AS DATE));
                UPDATE Estudiantes SET num_reservas = num_reservas + 1 WHERE email = '123';
        END

        -- Reserva 2
        IF NOT EXISTS(SELECT 1 FROM Reservas WHERE ISBN = '978-84-7615-689-2' AND estado IN ('Espera','Recoger'))
        BEGIN
                INSERT INTO Reservas (estado, email, ISBN, fecha_reserva)
                VALUES ('Espera', '123', '978-84-7615-689-2', CAST(GETDATE() AS DATE));
                UPDATE Estudiantes SET num_reservas = num_reservas + 1 WHERE email = '123';
        END

        -- Reserva 3
        IF NOT EXISTS(SELECT 1 FROM Reservas WHERE ISBN = '978-84-8322-855-0' AND estado IN ('Espera','Recoger'))
        BEGIN
                INSERT INTO Reservas (estado, email, ISBN, fecha_reserva)
                VALUES ('Espera', '123', '978-84-8322-855-0', CAST(GETDATE() AS DATE));
                UPDATE Estudiantes SET num_reservas = num_reservas + 1 WHERE email = '123';
        END
END
ELSE
BEGIN
        PRINT 'El usuario 123 ya tiene 3 o más reservas activas. No se insertan más.';
END

-- Intento de reserva 4 (debe ser rechazado por la lógica de la aplicación)
IF (SELECT COUNT(*) FROM Reservas WHERE email = '123' AND estado IN ('Espera','Recoger')) < 3
BEGIN
        INSERT INTO Reservas (estado, email, ISBN, fecha_reserva)
        VALUES ('Espera', '123', '978-84-291-6003-1', CAST(GETDATE() AS DATE));
        UPDATE Estudiantes SET num_reservas = num_reservas + 1 WHERE email = '123';
END
ELSE
BEGIN
        PRINT 'Rechazado: no se permite una cuarta reserva activa para 123.';
END

/* Escenario 2: cuando un libro pasa de Prestado -> Devuelto, la primera reserva en Espera se marca Recoger */
-- Simular devolución del libro A (978-84-9735-730-3)
UPDATE Prestamos SET estado = 'Devuelto', fecha_devolucion = CAST(DATEADD(day, -1, GETDATE()) AS DATE)
WHERE ISBN = '978-84-9735-730-3' AND estado = 'Activo';
-- poner libro disponible temporalmente
UPDATE Libros SET disponibilidad = 'Disponible' WHERE ISBN = '978-84-9735-730-3';

-- Buscar la reserva más antigua en 'Espera' para ese ISBN y pasarla a 'Recoger'
DECLARE @idReserva INT;
SELECT TOP 1 @idReserva = ID_reserva FROM Reservas WHERE ISBN = '978-84-9735-730-3' AND estado = 'Espera' ORDER BY fecha_reserva ASC;
IF @idReserva IS NOT NULL
BEGIN
        UPDATE Reservas SET estado = 'Recoger' WHERE ID_reserva = @idReserva;
        UPDATE Libros SET disponibilidad = 'Reservado' WHERE ISBN = '978-84-9735-730-3';
        PRINT 'Reserva promovida a Recoger y libro puesto en Reservado.';
END

/* Escenario 3: Caducidad de reserva si no se recoge en 7 días */
-- Crear una reserva vieja para simular caducidad
INSERT INTO Reservas (estado, email, ISBN, fecha_reserva)
VALUES ('Recoger', '1234', '978-84-7615-544-4', CAST(DATEADD(day, -10, GETDATE()) AS DATE));
UPDATE Libros SET disponibilidad = 'Reservado' WHERE ISBN = '978-84-7615-544-4';

-- Marcar caducadas las reservas con estado 'Recoger' con más de 7 días sin recogida
UPDATE Reservas
SET estado = 'Caducada'
WHERE estado = 'Recoger' AND fecha_reserva < CAST(DATEADD(day, -7, GETDATE()) AS DATE);

-- Restaurar disponibilidad a Disponible para los libros cuyos reservas caducaron
-- Según petición: los libros con reservas 'Caducada' se muestran como 'Reservado' en catálogo
UPDATE Libros
SET disponibilidad = 'Reservado'
WHERE ISBN IN (
        SELECT ISBN FROM Reservas WHERE estado = 'Caducada'
);

/* Consecuencias administrativas (ejemplos):
 - num_reservas en tabla Estudiantes incrementado por cada reserva creada.
 - disponibilidad de Libros cambia según reglas: Prestado/Reservado/Disponible/Retirado.
 - El sistema de aplicación debe prevenir más de 3 reservas y una reserva activa por ISBN.
*/

/* -------------------------------------------------- */
/* Préstamos adicionales para la cuenta '123' */
/* Insertamos varios préstamos (Activos, Vencido, Devuelto) y actualizamos contadores */

-- Selección de ISBNs para los préstamos adicionales
UPDATE Libros SET disponibilidad = 'Prestado' WHERE ISBN IN (
        '978-84-8322-340-1', -- Aprendizaje Automático
        '978-84-291-5788-8', -- Estructura de Computadores
        '978-84-9735-610-8', -- Sistemas Operativos Modernos
        '978-84-7615-544-4', -- Introducción a los Algoritmos
        '978-84-291-6312-4'  -- Geología Física
);

-- 1) Activos normales
INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga)
VALUES
('123', '978-84-8322-340-1', 'Activo', CAST(GETDATE() AS DATE), CAST(DATEADD(day, 14, GETDATE()) AS DATE), 0),
('123', '978-84-291-5788-8', 'Activo', CAST(GETDATE() AS DATE), CAST(DATEADD(day, 14, GETDATE()) AS DATE), 0),
('123', '978-84-9735-610-8', 'Activo', CAST(GETDATE() AS DATE), CAST(DATEADD(day, 14, GETDATE()) AS DATE), 0);

-- 2) Activo con prórroga utilizada
UPDATE Libros SET disponibilidad = 'Prestado' WHERE ISBN = '978-84-7615-544-4';
INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga)
VALUES ('123', '978-84-7615-544-4', 'Activo', CAST(DATEADD(day, -10, GETDATE()) AS DATE), CAST(DATEADD(day, 11, GETDATE()) AS DATE), 1);

-- 3) Vencido
UPDATE Libros SET disponibilidad = 'Prestado' WHERE ISBN = '978-84-291-6312-4';
INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga)
VALUES ('123', '978-84-291-6312-4', 'Vencido', CAST(DATEADD(day, -40, GETDATE()) AS DATE), CAST(DATEADD(day, -5, GETDATE()) AS DATE), 0);

-- 4) Devuelto (histórico)
INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga)
VALUES ('123', '978-84-291-6003-1', 'Devuelto', CAST(DATEADD(day, -30, GETDATE()) AS DATE), CAST(DATEADD(day, -10, GETDATE()) AS DATE), 0);
UPDATE Libros SET disponibilidad = 'Disponible' WHERE ISBN = '978-84-291-6003-1';

-- Actualizar contador de préstamos en Estudiantes (incrementar por los nuevos préstamos no devueltos)
UPDATE Estudiantes SET num_prestamos = num_prestamos + (
        SELECT COUNT(*) FROM Prestamos p WHERE p.email = '123' AND p.estado IN ('Activo','Vencido')
)
WHERE email = '123';

GO
