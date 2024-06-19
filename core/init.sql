
-- Create Database
CREATE DATABASE IF NOT EXISTS ANNODATA DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

USE ANNODATA;

-- Create Tables
CREATE TABLE IF NOT EXISTS dataset (
    dataset_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    data_type TINYINT NOT NULL  DEFAULT 0 COMMENT "0:IMAGE, 1:STATISTICS",
    data_desc VARCHAR(1000) NULL
)
    ENGINE=InnoDB
    DEFAULT CHARACTER SET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS label_field (
    label_field_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NULL,
    dataset_id INT NOT NULL,
    subject TINYINT NOT NULL DEFAULT 0 COMMENT "0: Box label, 1: Image label",
    type TINYINT NOT NULL DEFAULT 0 COMMENT"0: OD, 1: caption, 2: cls",
    duplicatable TINYINT(1) NOT NULL DEFAULT 0,
    detail VARCHAR(400) NULL,
    FOREIGN KEY(dataset_id) REFERENCES ANNODATA.dataset(dataset_id) ON DELETE CASCADE
)
    ENGINE=InnoDB
    DEFAULT CHARACTER SET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS image_data (
    image_data_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    dataset_id INT NOT NULL,
    filename VARCHAR(50) NOT NULL,
    image_fid VARCHAR(20) NOT NULL,
    image_url VARCHAR(200) NOT NULL,
    width SMALLINT NOT NULL,
    height SMALLINT NOT NULL,
    FOREIGN KEY(dataset_id) REFERENCES ANNODATA.dataset(dataset_id) ON DELETE CASCADE
)
    ENGINE=InnoDB
    DEFAULT CHARACTER SET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS label_data (
    label_data_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    image_data_id INT NOT NULL,
    label_field_id INT NOT NULL,
    ref_box_id INT NULL,
    is_box TINYINT(1) NOT NULL DEFAULT 0,
    coord VARCHAR(100) NULL,
    cls TINYINT NULL,
    caption VARCHAR(500) NULL,
    FOREIGN KEY(image_data_id) REFERENCES ANNODATA.image_data(image_data_id) ON DELETE CASCADE,
    FOREIGN KEY(label_field_id) REFERENCES ANNODATA.label_field(label_field_id) ON DELETE CASCADE
)
    ENGINE=InnoDB
    DEFAULT CHARACTER SET=utf8mb4 COLLATE=utf8mb4_general_ci;