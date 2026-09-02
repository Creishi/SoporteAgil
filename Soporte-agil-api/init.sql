CREATE TABLE tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL,
    estado VARCHAR(50) DEFAULT 'ABIERTO',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO tickets (titulo, descripcion, estado) 
VALUES ('Fallo de red en sucursal', 'El router principal no asigna IPs', 'ABIERTO');