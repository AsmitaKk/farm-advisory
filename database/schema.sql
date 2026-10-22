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

CREATE TABLE IF NOT EXISTS irrigation_profiles (
 id INT UNSIGNED NOT NULL AUTO_INCREMENT, user_email VARCHAR(255) NOT NULL, farmer_name VARCHAR(120) NOT NULL,
 state VARCHAR(80) NOT NULL DEFAULT 'Maharashtra', district VARCHAR(100) NOT NULL, taluka VARCHAR(100) NOT NULL, village VARCHAR(120) NOT NULL,
 latitude DECIMAL(9,6) NULL, longitude DECIMAL(9,6) NULL, crop_name VARCHAR(80) NOT NULL, area DECIMAL(10,2) NOT NULL,
 area_unit ENUM('acre','hectare') NOT NULL, soil_type ENUM('Black','Red','Sandy','Loamy','Clay') NOT NULL,
 irrigation_method ENUM('Drip','Sprinkler','Surface') NOT NULL, sowing_date DATE NOT NULL, growth_stage VARCHAR(60) NOT NULL,
 last_irrigation_date DATE NULL, last_irrigation_mm DECIMAL(8,2) NULL, soil_moisture DECIMAL(5,2) NULL,
 flow_rate_lph DECIMAL(12,2) NULL, updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 PRIMARY KEY (id), UNIQUE KEY uq_irrigation_profile_email (user_email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS irrigation_history (
 id INT UNSIGNED NOT NULL AUTO_INCREMENT, user_email VARCHAR(255) NOT NULL, irrigation_date DATE NOT NULL,
 depth_mm DECIMAL(8,2) NOT NULL, liters DECIMAL(14,2) NOT NULL, method VARCHAR(30) NOT NULL,
 notes VARCHAR(500) NULL, completed BOOLEAN NOT NULL DEFAULT TRUE, created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 PRIMARY KEY (id), KEY idx_irrigation_history_email_date (user_email, irrigation_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
