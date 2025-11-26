CREATE DATABASE IF NOT EXISTS  finaldb;

USE finaldb;

-- 1. Tabla de Actores
CREATE TABLE actores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE,
    nacionalidad VARCHAR(50)
);
-- 3. Tabla de Teatros
CREATE TABLE teatros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(150),
    ciudad VARCHAR(50)
);
-- 2. Tabla de Funciones
CREATE TABLE funciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    fecha DATE NOT NULL,
    teatro_id INT,
    precio DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (teatro_id) REFERENCES teatros(id) ON DELETE SET NULL
);



-- 4. Tabla de Roles
CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

-- 5. Tabla de Entradas
CREATE TABLE entradas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    funcion_id INT NOT NULL,
    fecha_compra DATE NOT NULL,
    cantidad INT NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (funcion_id) REFERENCES funciones(id) ON DELETE CASCADE
);

-- 6. Tabla de Asistencias
CREATE TABLE asistencias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    funcion_id INT NOT NULL,
    actor_id INT NOT NULL,
    role_id INT,
    FOREIGN KEY (funcion_id) REFERENCES funciones(id) ON DELETE CASCADE,
    FOREIGN KEY (actor_id) REFERENCES actores(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE SET NULL
);
