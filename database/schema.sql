CREATE TABLE IF NOT EXISTS users (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(120) NOT NULL,
    username VARCHAR(80) NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'farmer') NOT NULL DEFAULT 'farmer',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_users_email (email),
    UNIQUE KEY uq_users_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS crops (
    id VARCHAR(100) NOT NULL,
    name VARCHAR(120) NOT NULL,
    soil VARCHAR(120) NOT NULL,
    climate VARCHAR(120) NOT NULL,
    rainfall VARCHAR(80) NOT NULL,
    ph VARCHAR(40) NOT NULL,
    season VARCHAR(120) NOT NULL,
    `yield` VARCHAR(120) NOT NULL,
    description TEXT NOT NULL,
    image VARCHAR(500) NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS soils (
    id VARCHAR(100) NOT NULL,
    name VARCHAR(120) NOT NULL,
    color VARCHAR(80) NOT NULL,
    texture VARCHAR(80) NOT NULL,
    ph VARCHAR(40) NOT NULL,
    fertility VARCHAR(80) NOT NULL,
    moisture VARCHAR(80) NOT NULL,
    best_crops VARCHAR(500) NOT NULL,
    description TEXT NOT NULL,
    image VARCHAR(500) NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS fertilizers (
    id VARCHAR(100) NOT NULL,
    name VARCHAR(160) NOT NULL,
    type VARCHAR(100) NOT NULL,
    npk VARCHAR(40) NOT NULL,
    best_for VARCHAR(500) NOT NULL,
    `usage` TEXT NOT NULL,
    precautions TEXT NOT NULL,
    image VARCHAR(500) NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS market_data (
    id VARCHAR(100) NOT NULL,
    crop VARCHAR(160) NOT NULL,
    variety VARCHAR(160) NOT NULL,
    price_val DECIMAL(12,2) NOT NULL,
    trend ENUM('up', 'down', 'stable') NOT NULL DEFAULT 'stable',
    `change` VARCHAR(30) NOT NULL DEFAULT '0.0%',
    display_order INT NOT NULL DEFAULT 0,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS transactions (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_email VARCHAR(255) NOT NULL,
    crop_id VARCHAR(100) NULL,
    crop_name VARCHAR(160) NOT NULL,
    action ENUM('BUY', 'SELL') NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    quantity DECIMAL(12,2) NOT NULL,
    total DECIMAL(14,2) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Confirmed',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_transactions_email (user_email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS farmer_queries (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(255) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    status ENUM('Pending', 'Resolved') NOT NULL DEFAULT 'Pending',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_queries_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
