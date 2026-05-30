-- ============================================================
--  TaskFlow Database Setup Script
--  Run once before starting the app: mysql -u root -p < db_setup.sql
-- ============================================================

CREATE DATABASE IF NOT EXISTS task_manager_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE task_manager_db;

-- Flask-SQLAlchemy will auto-create tables on first run,
-- but you can also create them manually here.

CREATE TABLE IF NOT EXISTS users (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    username   VARCHAR(80)  NOT NULL UNIQUE,
    email      VARCHAR(120) NOT NULL UNIQUE,
    password   VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS tasks (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    title       VARCHAR(200) NOT NULL,
    description TEXT,
    due_date    DATE,
    status      VARCHAR(20) NOT NULL DEFAULT 'Pending',
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id     INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_status (user_id, status)
) ENGINE=InnoDB;

-- Optional: seed a test user (password: test123)
-- (bcrypt hash of 'test123')
-- INSERT INTO users (username, email, password) VALUES
--   ('testuser', 'test@example.com', '$2b$12$...');

SELECT 'Database setup complete!' AS message;
