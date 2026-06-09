USE BibliotecaDB;
GO

DELETE FROM Prestamos WHERE email IN ('123','1234','smartm00@estudiantes.unileon.es');
DELETE FROM Reservas  WHERE email IN ('123','1234','smartm00@estudiantes.unileon.es');
DELETE FROM Sanciones WHERE email IN ('123','1234','smartm00@estudiantes.unileon.es');

-- Restablecer a 'Disponible' todos los libros que toca este script
DELETE FROM Retirados WHERE ISBN IN ('978-84-291-6124-3');
UPDATE Libros SET disponibilidad = 'Disponible' WHERE ISBN IN (
    '978-84-7615-689-2','978-84-8322-855-0','978-84-9735-730-3','978-84-291-5032-2',
    '978-84-291-4198-6','978-84-9835-203-4','978-84-376-0812-9','978-84-291-6124-3',
    '978-84-7615-544-4','978-84-9732-430-9','978-84-291-1720-2','978-84-9732-567-2',
    '978-84-9835-780-0'
);
GO

IF NOT EXISTS (SELECT 1 FROM Usuarios WHERE email='123')
    INSERT INTO Usuarios (contrasena, email, nombre, apellidos, tipo) VALUES ('123','123','Miguel','Gómez Pérez','Estudiante');
IF NOT EXISTS (SELECT 1 FROM Usuarios WHERE email='1234')
    INSERT INTO Usuarios (contrasena, email, nombre, apellidos, tipo) VALUES ('1234','1234','Elena','Rodríguez Martínez','Estudiante');
IF NOT EXISTS (SELECT 1 FROM Usuarios WHERE email='smartm00@estudiantes.unileon.es')
    INSERT INTO Usuarios (contrasena, email, nombre, apellidos, tipo) VALUES ('pass_ing','smartm00@estudiantes.unileon.es','Sara','Martín Morales','Estudiante');

IF NOT EXISTS (SELECT 1 FROM Estudiantes WHERE email='123')
    INSERT INTO Estudiantes (email, num_prestamos, num_reservas, sanciones) VALUES ('123',0,0,0);
IF NOT EXISTS (SELECT 1 FROM Estudiantes WHERE email='1234')
    INSERT INTO Estudiantes (email, num_prestamos, num_reservas, sanciones) VALUES ('1234',0,0,0);
IF NOT EXISTS (SELECT 1 FROM Estudiantes WHERE email='smartm00@estudiantes.unileon.es')
    INSERT INTO Estudiantes (email, num_prestamos, num_reservas, sanciones) VALUES ('smartm00@estudiantes.unileon.es',0,0,0);
GO

UPDATE Libros SET disponibilidad = 'Prestado' WHERE ISBN = '978-84-7615-689-2'; -- Bases de Datos
INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga)
VALUES ('123', '978-84-7615-689-2', 'Activo',
        CAST(GETDATE() AS DATE), CAST(DATEADD(day, 14, GETDATE()) AS DATE), 0);

-- 2.2  Préstamo que VENCE EN 2 DÍAS  -> debe aparecer RESALTADO en "Mis préstamos"
UPDATE Libros SET disponibilidad = 'Prestado' WHERE ISBN = '978-84-8322-855-0'; -- Ingeniería del Software
INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga)
VALUES ('123', '978-84-8322-855-0', 'Activo',
        CAST(DATEADD(day, -12, GETDATE()) AS DATE), CAST(DATEADD(day, 2, GETDATE()) AS DATE), 0);

-- 2.3  Préstamo YA PRORROGADO (prorroga=1, 21 días)  -> demostrar que NO se puede prorrogar otra vez
UPDATE Libros SET disponibilidad = 'Prestado' WHERE ISBN = '978-84-9735-730-3'; -- Redes de Computadores
INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga)
VALUES ('123', '978-84-9735-730-3', 'Activo',
        CAST(DATEADD(day, -3, GETDATE()) AS DATE), CAST(DATEADD(day, 18, GETDATE()) AS DATE), 1);

-- 2.4  Préstamo ACTIVO SIN prórroga y SIN reserva  -> PRORROGAR EN VIVO (debe funcionar)
UPDATE Libros SET disponibilidad = 'Prestado' WHERE ISBN = '978-84-291-5032-2'; -- Cálculo Diferencial
INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga)
VALUES ('123', '978-84-291-5032-2', 'Activo',
        CAST(DATEADD(day, -4, GETDATE()) AS DATE), CAST(DATEADD(day, 10, GETDATE()) AS DATE), 0);

-- 2.5  Préstamo VENCIDO (fecha pasada)  -> ejemplo de retraso (sanción al devolver)
UPDATE Libros SET disponibilidad = 'Prestado' WHERE ISBN = '978-84-291-4198-6'; -- Mecánica Clásica
INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga)
VALUES ('123', '978-84-291-4198-6', 'Vencido',
        CAST(DATEADD(day, -30, GETDATE()) AS DATE), CAST(DATEADD(day, -2, GETDATE()) AS DATE), 0);
GO

UPDATE Libros SET disponibilidad = 'Prestado' WHERE ISBN = '978-84-9835-203-4'; -- Anatomía Humana
INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga)
VALUES ('smartm00@estudiantes.unileon.es', '978-84-9835-203-4', 'Activo',
        CAST(DATEADD(day, -5, GETDATE()) AS DATE), CAST(DATEADD(day, 9, GETDATE()) AS DATE), 0);
INSERT INTO Reservas (estado, email, ISBN, fecha_reserva)
VALUES ('Espera', '123', '978-84-9835-203-4', CAST(DATEADD(day, -1, GETDATE()) AS DATE));

UPDATE Libros SET disponibilidad = 'Reservado' WHERE ISBN = '978-84-376-0812-9'; -- La Casa de Bernarda Alba
INSERT INTO Reservas (estado, email, ISBN, fecha_reserva)
VALUES ('Recoger', '123', '978-84-376-0812-9', CAST(DATEADD(day, -2, GETDATE()) AS DATE));


UPDATE Libros SET disponibilidad = 'Reservado' WHERE ISBN = '978-84-291-1720-2'; -- La República
INSERT INTO Reservas (estado, email, ISBN, fecha_reserva)
VALUES ('Recoger', 'smartm00@estudiantes.unileon.es', '978-84-291-1720-2', CAST(DATEADD(day, -1, GETDATE()) AS DATE));

UPDATE Libros SET disponibilidad = 'Reservado' WHERE ISBN = '978-84-9732-567-2'; -- Historia de la Arquitectura
INSERT INTO Reservas (estado, email, ISBN, fecha_reserva)
VALUES ('Recoger', 'smartm00@estudiantes.unileon.es', '978-84-9732-567-2', CAST(DATEADD(day, -3, GETDATE()) AS DATE));

UPDATE Libros SET disponibilidad = 'Reservado' WHERE ISBN = '978-84-9835-780-0'; -- El Origen de las Especies
INSERT INTO Reservas (estado, email, ISBN, fecha_reserva)
VALUES ('Caducada', '123', '978-84-9835-780-0', CAST(DATEADD(day, -10, GETDATE()) AS DATE));
GO

INSERT INTO Sanciones (tipo, estado, fecha_inicio, duracion, email)
VALUES ('Retraso', 'Activa', CAST(GETDATE() AS DATE), 10, '1234');

-- Sanción CUMPLIDA por daño (Roto = 30 días), histórica
INSERT INTO Sanciones (tipo, estado, fecha_inicio, duracion, email)
VALUES ('Daño (Roto)', 'Cumplida', CAST(DATEADD(day, -45, GETDATE()) AS DATE), 30, '1234');
GO

UPDATE Libros SET disponibilidad = 'Retirado' WHERE ISBN = '978-84-291-6124-3'; -- Dibujo Técnico Industrial
INSERT INTO Retirados (ISBN, motivo, fecha_retiro)
VALUES ('978-84-291-6124-3', 'Ejemplar deteriorado y edición desactualizada', CAST(GETDATE() AS DATE));
GO

INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga)
VALUES ('123', '978-84-7615-544-4', 'Devuelto',
        CAST(DATEADD(day, -17, GETDATE()) AS DATE), CAST(DATEADD(day, -3, GETDATE()) AS DATE), 0);
-- (el libro queda 'Disponible', ya restablecido en la limpieza)
GO

INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga) VALUES
-- --- ÚLTIMA SEMANA (0-6 días) --- (Informática manda)
('123',                              '978-84-7615-689-2', 'Devuelto', CAST(DATEADD(day,-1,GETDATE()) AS DATE), CAST(GETDATE() AS DATE), 0),
('smartm00@estudiantes.unileon.es',  '978-84-8322-855-0', 'Devuelto', CAST(DATEADD(day,-2,GETDATE()) AS DATE), CAST(GETDATE() AS DATE), 0),
('123',                              '978-84-8322-783-6', 'Devuelto', CAST(DATEADD(day,-3,GETDATE()) AS DATE), CAST(GETDATE() AS DATE), 0),
('smartm00@estudiantes.unileon.es',  '978-84-291-6003-1', 'Devuelto', CAST(DATEADD(day,-4,GETDATE()) AS DATE), CAST(GETDATE() AS DATE), 0),
('123',                              '978-84-291-5032-2', 'Devuelto', CAST(DATEADD(day,-2,GETDATE()) AS DATE), CAST(GETDATE() AS DATE), 0),
('smartm00@estudiantes.unileon.es',  '978-84-9732-052-3', 'Devuelto', CAST(DATEADD(day,-5,GETDATE()) AS DATE), CAST(GETDATE() AS DATE), 0),
('123',                              '978-84-9835-203-4', 'Devuelto', CAST(DATEADD(day,-3,GETDATE()) AS DATE), CAST(GETDATE() AS DATE), 0),
('smartm00@estudiantes.unileon.es',  '978-84-9835-944-6', 'Devuelto', CAST(DATEADD(day,-6,GETDATE()) AS DATE), CAST(GETDATE() AS DATE), 0),
('123',                              '978-84-291-4198-6', 'Devuelto', CAST(DATEADD(day,-4,GETDATE()) AS DATE), CAST(GETDATE() AS DATE), 0),
('smartm00@estudiantes.unileon.es',  '978-84-376-0812-9', 'Devuelto', CAST(DATEADD(day,-5,GETDATE()) AS DATE), CAST(GETDATE() AS DATE), 0),
-- --- ÚLTIMO MES (8-28 días) ---
('123',                              '978-84-9735-730-3', 'Devuelto', CAST(DATEADD(day,-10,GETDATE()) AS DATE), CAST(DATEADD(day,-1,GETDATE()) AS DATE), 0),
('smartm00@estudiantes.unileon.es',  '978-84-7615-544-4', 'Devuelto', CAST(DATEADD(day,-12,GETDATE()) AS DATE), CAST(DATEADD(day,-1,GETDATE()) AS DATE), 0),
('123',                              '978-84-7615-402-7', 'Devuelto', CAST(DATEADD(day,-14,GETDATE()) AS DATE), CAST(DATEADD(day,-2,GETDATE()) AS DATE), 0),
('smartm00@estudiantes.unileon.es',  '978-84-291-5015-5', 'Devuelto', CAST(DATEADD(day,-18,GETDATE()) AS DATE), CAST(DATEADD(day,-3,GETDATE()) AS DATE), 0),
('123',                              '978-84-291-3985-3', 'Devuelto', CAST(DATEADD(day,-20,GETDATE()) AS DATE), CAST(DATEADD(day,-5,GETDATE()) AS DATE), 0),
('smartm00@estudiantes.unileon.es',  '978-84-9835-780-0', 'Devuelto', CAST(DATEADD(day,-22,GETDATE()) AS DATE), CAST(DATEADD(day,-8,GETDATE()) AS DATE), 0),
('123',                              '978-84-7615-771-4', 'Devuelto', CAST(DATEADD(day,-16,GETDATE()) AS DATE), CAST(DATEADD(day,-2,GETDATE()) AS DATE), 0),
('smartm00@estudiantes.unileon.es',  '978-84-9835-320-8', 'Devuelto', CAST(DATEADD(day,-25,GETDATE()) AS DATE), CAST(DATEADD(day,-11,GETDATE()) AS DATE), 0),
('123',                              '978-84-7615-742-4', 'Devuelto', CAST(DATEADD(day,-26,GETDATE()) AS DATE), CAST(DATEADD(day,-12,GETDATE()) AS DATE), 0),
-- --- ÚLTIMOS 3 MESES (35-85 días) ---
('123',                              '978-84-7615-689-2', 'Devuelto', CAST(DATEADD(day,-40,GETDATE()) AS DATE), CAST(DATEADD(day,-26,GETDATE()) AS DATE), 0),
('smartm00@estudiantes.unileon.es',  '978-84-8322-855-0', 'Devuelto', CAST(DATEADD(day,-45,GETDATE()) AS DATE), CAST(DATEADD(day,-31,GETDATE()) AS DATE), 0),
('123',                              '978-84-291-6908-5', 'Devuelto', CAST(DATEADD(day,-50,GETDATE()) AS DATE), CAST(DATEADD(day,-36,GETDATE()) AS DATE), 0),
('smartm00@estudiantes.unileon.es',  '978-84-9835-843-2', 'Devuelto', CAST(DATEADD(day,-55,GETDATE()) AS DATE), CAST(DATEADD(day,-41,GETDATE()) AS DATE), 0),
('123',                              '978-84-291-2210-7', 'Devuelto', CAST(DATEADD(day,-60,GETDATE()) AS DATE), CAST(DATEADD(day,-46,GETDATE()) AS DATE), 0),
('smartm00@estudiantes.unileon.es',  '978-84-9835-178-5', 'Devuelto', CAST(DATEADD(day,-65,GETDATE()) AS DATE), CAST(DATEADD(day,-51,GETDATE()) AS DATE), 0),
('123',                              '978-84-9732-430-9', 'Devuelto', CAST(DATEADD(day,-70,GETDATE()) AS DATE), CAST(DATEADD(day,-56,GETDATE()) AS DATE), 0),
('smartm00@estudiantes.unileon.es',  '978-84-291-4690-5', 'Devuelto', CAST(DATEADD(day,-75,GETDATE()) AS DATE), CAST(DATEADD(day,-61,GETDATE()) AS DATE), 0),
('123',                              '978-84-7615-561-1', 'Devuelto', CAST(DATEADD(day,-80,GETDATE()) AS DATE), CAST(DATEADD(day,-66,GETDATE()) AS DATE), 0),
('smartm00@estudiantes.unileon.es',  '978-84-291-4025-5', 'Devuelto', CAST(DATEADD(day,-85,GETDATE()) AS DATE), CAST(DATEADD(day,-71,GETDATE()) AS DATE), 0);
GO

UPDATE Estudiantes SET
    num_prestamos = (SELECT COUNT(*) FROM Prestamos WHERE email='123'  AND estado IN ('Activo','Vencido')),
    num_reservas  = (SELECT COUNT(*) FROM Reservas  WHERE email='123'  AND estado IN ('Espera','Recoger')),
    sanciones     = (SELECT COUNT(*) FROM Sanciones WHERE email='123'  AND estado='Activa')
WHERE email='123';

UPDATE Estudiantes SET
    num_prestamos = (SELECT COUNT(*) FROM Prestamos WHERE email='smartm00@estudiantes.unileon.es' AND estado IN ('Activo','Vencido')),
    num_reservas  = (SELECT COUNT(*) FROM Reservas  WHERE email='smartm00@estudiantes.unileon.es' AND estado IN ('Espera','Recoger')),
    sanciones     = (SELECT COUNT(*) FROM Sanciones WHERE email='smartm00@estudiantes.unileon.es' AND estado='Activa')
WHERE email='smartm00@estudiantes.unileon.es';

UPDATE Estudiantes SET
    num_prestamos = (SELECT COUNT(*) FROM Prestamos WHERE email='1234' AND estado IN ('Activo','Vencido')),
    num_reservas  = (SELECT COUNT(*) FROM Reservas  WHERE email='1234' AND estado IN ('Espera','Recoger')),
    sanciones     = (SELECT COUNT(*) FROM Sanciones WHERE email='1234' AND estado='Activa')
WHERE email='1234';
GO