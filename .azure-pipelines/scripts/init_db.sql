-- Crear la base de datos si no existe
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT 
      FROM pg_catalog.pg_database
      WHERE datname = 'recommended') THEN
      CREATE DATABASE recommended;
   END IF;
END
$do$;

-- Crear la tabla users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    identification_number VARCHAR(255) UNIQUE,
    slug VARCHAR(255) UNIQUE,
    video TEXT,
    email VARCHAR(255) UNIQUE,
    gender VARCHAR(1),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Crear la tabla resumes
CREATE TABLE IF NOT EXISTS resumes (
    id SERIAL PRIMARY KEY,
    user_id INT,
    name VARCHAR(255),
    type VARCHAR(50),
    video TEXT,
    views INT,
    created_at TIMESTAMP
    --CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Crear la tabla profiles
CREATE TABLE IF NOT EXISTS profiles (
    id SERIAL PRIMARY KEY,
    user_id INT,
    onboarding_goal VARCHAR(255),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    views INT
    --CONSTRAINT fk_profile_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Crear la tabla challenges
CREATE TABLE IF NOT EXISTS challenges (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    status VARCHAR(50),
    opencall_objective VARCHAR(255),
    created_at TIMESTAMP
);
