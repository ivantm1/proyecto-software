-- =============================================================================
--  DATOS DE PRUEBA COMPLEMENTARIOS — BibliotecaDB
--  Cuentas principales: 1 (Admin), 12 (Bibliotecario), 123 (Estudiante Miguel)
--  También se usan: 1234 (Estudiante Elena) y otros estudiantes existentes
-- =============================================================================

USE BibliotecaDB;
GO

-- =============================================================================
--  BLOQUE 1 — PRÉSTAMOS ACTIVOS (estado='Activo', fecha devolución futura)
--  Caso: libro prestado sin incidencias, el alumno aún tiene tiempo
-- =============================================================================

-- Miguel (123) tiene 3 libros activos
INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga) VALUES
('123', '978-84-291-5032-2', 'Activo', DATEADD(day,-5,GETDATE()), DATEADD(day,9,GETDATE()),  0),  -- Cálculo Diferencial
('123', '978-84-9835-944-6', 'Activo', DATEADD(day,-3,GETDATE()), DATEADD(day,11,GETDATE()), 0),  -- Visión por Computador
('123', '978-84-9735-730-3', 'Activo', DATEADD(day,-1,GETDATE()), DATEADD(day,13,GETDATE()), 0);  -- Redes de Computadores

UPDATE Libros SET disponibilidad='Prestado' WHERE ISBN IN (
    '978-84-291-5032-2','978-84-9835-944-6','978-84-9735-730-3'
);

-- Elena (1234) tiene 2 libros activos
INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga) VALUES
('1234', '978-84-291-4198-6', 'Activo', DATEADD(day,-7,GETDATE()), DATEADD(day,7,GETDATE()),  0),  -- Mecánica Clásica
('1234', '978-84-8322-337-1', 'Activo', DATEADD(day,-2,GETDATE()), DATEADD(day,12,GETDATE()), 0);  -- Microbiología

UPDATE Libros SET disponibilidad='Prestado' WHERE ISBN IN (
    '978-84-291-4198-6','978-84-8322-337-1'
);

-- =============================================================================
--  BLOQUE 2 — PRÉSTAMOS CON PRÓRROGA (prorroga=1)
--  Caso: el alumno solicitó prórroga, nuevo plazo extendido
-- =============================================================================

-- Miguel (123) tiene 1 préstamo prorrogado
INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga) VALUES
('123', '978-84-7615-544-4', 'Activo', DATEADD(day,-14,GETDATE()), DATEADD(day,14,GETDATE()), 1); -- Algoritmos (prorrogado)

UPDATE Libros SET disponibilidad='Prestado' WHERE ISBN='978-84-7615-544-4';

-- =============================================================================
--  BLOQUE 3 — PRÉSTAMOS VENCIDOS (estado='Vencido', fecha pasada)
--  Caso: el alumno no devolvió a tiempo, el trigger lo marca automáticamente
-- =============================================================================

-- Miguel (123) tiene 1 préstamo vencido
INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga) VALUES
('123', '978-84-291-7842-6', 'Vencido', DATEADD(day,-20,GETDATE()), DATEADD(day,-6,GETDATE()), 0); -- Ecología (vencido)

UPDATE Libros SET disponibilidad='Prestado' WHERE ISBN='978-84-291-7842-6';

-- Elena (1234) tiene 1 préstamo vencido
INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga) VALUES
('1234', '978-84-9835-780-0', 'Vencido', DATEADD(day,-25,GETDATE()), DATEADD(day,-11,GETDATE()), 0); -- Patología (vencido)

UPDATE Libros SET disponibilidad='Prestado' WHERE ISBN='978-84-9835-780-0';

-- =============================================================================
--  BLOQUE 4 — PRÉSTAMOS DEVUELTOS (estado='Devuelto')
--  Caso: historial de devoluciones pasadas para ver en "Mis Préstamos"
-- =============================================================================

-- Miguel (123) — historial de devoluciones
INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga) VALUES
('123', '978-84-8322-910-6', 'Devuelto', DATEADD(day,-60,GETDATE()), DATEADD(day,-46,GETDATE()), 0), -- Probabilidad
('123', '978-84-291-1720-2', 'Devuelto', DATEADD(day,-45,GETDATE()), DATEADD(day,-31,GETDATE()), 0), -- La República
('123', '978-84-376-0494-7', 'Devuelto', DATEADD(day,-30,GETDATE()), DATEADD(day,-16,GETDATE()), 0); -- Don Quijote

-- Elena (1234) — historial de devoluciones
INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga) VALUES
('1234', '978-84-9735-089-2', 'Devuelto', DATEADD(day,-50,GETDATE()), DATEADD(day,-36,GETDATE()), 0), -- Historia Música
('1234', '978-84-8322-240-4', 'Devuelto', DATEADD(day,-35,GETDATE()), DATEADD(day,-21,GETDATE()), 0); -- Ética a Nicómaco

-- Otros estudiantes — historial variado
INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga) VALUES
('smartm00@estudiantes.unileon.es', '978-84-9835-821-0', 'Devuelto', DATEADD(day,-40,GETDATE()), DATEADD(day,-26,GETDATE()), 0),
('dferns00@estudiantes.unileon.es', '978-84-291-3587-2', 'Devuelto', DATEADD(day,-55,GETDATE()), DATEADD(day,-41,GETDATE()), 0);

-- =============================================================================
--  BLOQUE 5 — RESERVAS EN ESTADO 'Pendiente'
--  Caso: alumno reservó un libro que está prestado, aún no se devolvió
-- =============================================================================

-- Miguel (123) reserva un libro que está prestado por Elena
-- '978-84-291-4198-6' = Mecánica Clásica (prestado por Elena, activo)
INSERT INTO Reservas (email, ISBN, fecha_reserva, estado) VALUES
('123', '978-84-291-4198-6', DATEADD(day,-3,GETDATE()), 'Pendiente');

-- Elena (1234) reserva un libro prestado por Miguel
-- '978-84-9835-944-6' = Visión por Computador (prestado por Miguel, activo)
INSERT INTO Reservas (email, ISBN, fecha_reserva, estado) VALUES
('1234', '978-84-9835-944-6', DATEADD(day,-1,GETDATE()), 'Pendiente');

-- Otro estudiante reserva libro prestado por Miguel (vencido)
-- '978-84-291-7842-6' = Ecología (vencido por Miguel)
INSERT INTO Reservas (email, ISBN, fecha_reserva, estado) VALUES
('smartm00@estudiantes.unileon.es', '978-84-291-7842-6', DATEADD(day,-2,GETDATE()), 'Pendiente');

-- =============================================================================
--  BLOQUE 6 — RESERVAS EN ESTADO 'Espera'
--  Caso: libro devuelto pero el alumno aún no lo ha recogido (< 7 días)
--  El libro queda disponible en la biblioteca esperando al alumno con reserva
-- =============================================================================

-- Libro '978-84-291-5560-0' = Urgencias en Medicina — devuelto ayer, reservado por Miguel
-- Simula: otro alumno lo tenía, lo devolvió, y Miguel tiene 6 días para recogerlo
UPDATE Libros SET disponibilidad='Reservado' WHERE ISBN='978-84-291-5560-0';

INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga) VALUES
('dferns00@estudiantes.unileon.es', '978-84-291-5560-0', 'Devuelto',
 DATEADD(day,-15,GETDATE()), DATEADD(day,-1,GETDATE()), 0);

INSERT INTO Reservas (email, ISBN, fecha_reserva, estado) VALUES
('123', '978-84-291-5560-0', DATEADD(day,-1,GETDATE()), 'Espera');


-- Libro '978-84-291-6908-5' = Derecho Constitucional — devuelto hace 3 días, reservado por Elena
UPDATE Libros SET disponibilidad='Reservado' WHERE ISBN='978-84-291-6908-5';

INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga) VALUES
('pcanol00@estudiantes.unileon.es', '978-84-291-6908-5', 'Devuelto',
 DATEADD(day,-17,GETDATE()), DATEADD(day,-3,GETDATE()), 0);

INSERT INTO Reservas (email, ISBN, fecha_reserva, estado) VALUES
('1234', '978-84-291-6908-5', DATEADD(day,-3,GETDATE()), 'Espera');

-- =============================================================================
--  BLOQUE 6B — RESERVAS EN ESTADO 'Recoger'
--  Caso: libro devuelto y disponible, pendiente de recogida por el alumno con reserva
--  El libro está apartado en la biblioteca (disponibilidad='Reservado'), listo para recoger
-- =============================================================================

-- Libro '978-84-9835-203-4' = Anatomía Humana — devuelto hace 2 días, reservado por David
UPDATE Libros SET disponibilidad='Reservado' WHERE ISBN='978-84-9835-203-4';

INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga) VALUES
('jvazqh00@estudiantes.unileon.es', '978-84-9835-203-4', 'Devuelto',
 DATEADD(day,-10,GETDATE()), DATEADD(day,-2,GETDATE()), 0);

INSERT INTO Reservas (email, ISBN, fecha_reserva, estado) VALUES
('dferns00@estudiantes.unileon.es', '978-84-9835-203-4', DATEADD(day,-2,GETDATE()), 'Recoger');

-- Libro '978-84-291-3985-3' = Harrison: Principios de Medicina Interna — devuelto hace 1 día, reservado por Sara
UPDATE Libros SET disponibilidad='Reservado' WHERE ISBN='978-84-291-3985-3';

INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga) VALUES
('pcanol00@estudiantes.unileon.es', '978-84-291-3985-3', 'Devuelto',
 DATEADD(day,-8,GETDATE()), DATEADD(day,-1,GETDATE()), 0);

INSERT INTO Reservas (email, ISBN, fecha_reserva, estado) VALUES
('smartm00@estudiantes.unileon.es', '978-84-291-3985-3', DATEADD(day,-1,GETDATE()), 'Recoger');

-- Libro '978-84-9835-612-4' = Farmacología Básica y Clínica — devuelto hoy mismo, reservado por Laura
UPDATE Libros SET disponibilidad='Reservado' WHERE ISBN='978-84-9835-612-4';

INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga) VALUES
('amends00@estudiantes.unileon.es', '978-84-9835-612-4', 'Devuelto',
 DATEADD(day,-5,GETDATE()), CAST(GETDATE() AS DATE), 0);

INSERT INTO Reservas (email, ISBN, fecha_reserva, estado) VALUES
('ldiazf00@estudiantes.unileon.es', '978-84-9835-612-4', CAST(GETDATE() AS DATE), 'Recoger');

-- Libro '978-84-9835-203-4' = Anatomía Humana — devuelto hace 2 días, reservado por David
-- =============================================================================
--  BLOQUE 7 — RESERVAS EN ESTADO 'Espera' EXPIRADA (> 7 días sin recoger)
--  Caso: el alumno dejó pasar más de 7 días → la lógica debe pasarla a 'Caducada'
--        Se inserta en 'Espera' para que la app la detecte y cambie automáticamente
-- =============================================================================

-- Libro '978-84-9835-310-9' = Armonía (Música) — en espera desde hace 9 días (expirada)
UPDATE Libros SET disponibilidad='Reservado' WHERE ISBN='978-84-9835-310-9';

INSERT INTO Prestamos (email, ISBN, estado, fecha_prestamo, fecha_devolucion, prorroga) VALUES
('lruizm00@estudiantes.unileon.es', '978-84-9835-310-9', 'Devuelto',
 DATEADD(day,-25,GETDATE()), DATEADD(day,-9,GETDATE()), 0);

INSERT INTO Reservas (email, ISBN, fecha_reserva, estado) VALUES
('123', '978-84-9835-310-9', DATEADD(day,-9,GETDATE()), 'Espera');  -- 9 días → expirada

-- =============================================================================
--  BLOQUE 8 — RESERVAS 'Caducada' (historial)
--  Caso: reservas expiradas que aparecen en el historial del alumno
-- =============================================================================

INSERT INTO Reservas (email, ISBN, fecha_reserva, estado) VALUES
-- Miguel (123) — reservas pasadas cumplidas
('123', '978-84-8322-910-6', DATEADD(day,-70,GETDATE()), 'Caducada'),  -- Probabilidad
('123', '978-84-291-1720-2', DATEADD(day,-55,GETDATE()), 'Caducada'),  -- La República
-- Elena (1234) — reservas pasadas caducadas
('1234', '978-84-9735-089-2', DATEADD(day,-65,GETDATE()), 'Caducada'), -- Historia Música
('1234', '978-84-291-5032-2', DATEADD(day,-40,GETDATE()), 'Caducada'), -- Cálculo (ya está prestado por Miguel, historial OK)
-- Otros
('smartm00@estudiantes.unileon.es', '978-84-7615-544-4', DATEADD(day,-30,GETDATE()), 'Caducada');

-- =============================================================================
--  BLOQUE 9 — SANCIONES
--  Casos: sanción activa (bloquea préstamos/reservas) y sanción cumplida (historial)
-- =============================================================================

-- Elena (1234) tiene una sanción ACTIVA por retraso (bloquea préstamos y reservas)
INSERT INTO Sanciones (tipo, estado, fecha_inicio, duracion, email) VALUES
('Retraso en devolución', 'Activa', DATEADD(day,-5,GETDATE()), 14, '1234');

-- Miguel (123) tiene una sanción CUMPLIDA (solo historial, no le bloquea)
INSERT INTO Sanciones (tipo, estado, fecha_inicio, duracion, email) VALUES
('Retraso en devolución', 'Cumplida', DATEADD(day,-60,GETDATE()), 7, '123');

-- Otro estudiante con sanción activa por daño
INSERT INTO Sanciones (tipo, estado, fecha_inicio, duracion, email) VALUES
('Libro dañado', 'Activa', DATEADD(day,-2,GETDATE()), 30, 'smartm00@estudiantes.unileon.es');

-- Otro con sanción cumplida por daño (historial)
INSERT INTO Sanciones (tipo, estado, fecha_inicio, duracion, email) VALUES
('Libro roto', 'Cumplida', DATEADD(day,-90,GETDATE()), 60, 'dferns00@estudiantes.unileon.es');

-- =============================================================================
--  BLOQUE 10 — LIBROS RETIRADOS
--  Caso: libros dados de baja del catálogo por el bibliotecario
-- =============================================================================

UPDATE Libros SET disponibilidad='Retirado' WHERE ISBN IN (
    '978-84-291-3340-0',   -- El Arte del Siglo XX
    '978-84-9832-567-2'    -- (si no existe, SQL simplemente no actualiza nada)
);

INSERT INTO Retirados (ISBN, motivo, fecha_retiro) VALUES
('978-84-291-3340-0', 'Ejemplar deteriorado, páginas rotas y portada dañada', DATEADD(day,-10,GETDATE()));

-- =============================================================================
--  BLOQUE 11 — LIBRO DISPONIBLE SIN INCIDENCIAS (referencia limpia)
--  Caso: libro disponible para probar el flujo completo de reserva/préstamo
--        desde cero en las cuentas de prueba
-- =============================================================================
-- Los libros no mencionados arriba siguen en estado 'Disponible' por defecto.
-- Ejemplos disponibles para pruebas manuales:
--   '978-84-7615-402-7'  Matemáticas Discretas       (Disponible)
--   '978-84-291-4310-2'  Fisicoquímica                (Disponible)
--   '978-84-291-2450-7'  Psicopatología General       (Disponible)
--   '978-84-9835-821-0'  IA: Enfoque Moderno          (Disponible)
--   '978-84-376-0494-7'  Don Quijote                  (Disponible)
--   '978-84-9732-788-1'  Cien Años de Soledad         (Disponible)

--  CUENTA 1234 (Estudiante Elena):
--    Préstamos activos    : Mecánica Clásica, Microbiología
--    Préstamo vencido     : Patología Estructural
--    Devoluciones pasadas : Historia de la Música, Ética a Nicómaco
--    Reserva Pendiente    : Visión por Computador (prestado por Miguel)
--    Reserva Espera (<7d) : Derecho Constitucional (recogida pendiente)
--    Reservas Caducadas   : Historia de la Música, Cálculo (historial expirado)
--    Sanciones            : 1 ACTIVA por retraso (bloquea préstamos y reservas)
--
--  CUENTA 12 (Bibliotecario Pepe):
--    Puede ver en "Libros Reservados" TODAS las reservas del sistema:
--      - Reservas Pendientes de 123, 1234 y smartm00
--      - Reservas en Espera de 123 y 1234 (incluyendo la expirada)
--      - Reservas en Recoger de David, Sara y Laura (libros listos en biblioteca)
--      - Historial de Caducadas de todos
--    Puede gestionar devoluciones de cualquier ISBN activo/vencido
--    Puede hacer préstamos directos desde "Gestionar Estudiante"
--
--  CASOS ESPECIALES PARA PROBAR:
--    1. Devolver '978-84-291-4198-6' (Mecánica) → reserva de 123 pasa a 'Espera'
--    2. Miguel (123) pide prestado '978-84-291-5560-0' (Urgencias) → reserva se elimina
--    3. Elena (1234) intenta reservar/prestar → bloqueada por sanción activa
--    4. Abrir "Libros Reservados" como Pepe (12) → debe mostrar todas las reservas activas e historial
--    5. Armonía (ISBN 978-84-9835-310-9) → reserva expirada, la app la debe pasar a 'Caducada'
--    6. Libro en 'Recoger' (ej. '978-84-9835-203-4') → David (dferns00) debe poder verlo y recogerlo
--    7. Libro disponible '978-84-376-0494-7' (Don Quijote) → flujo nuevo préstamo/reserva
--
-- =============================================================================