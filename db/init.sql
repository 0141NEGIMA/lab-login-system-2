# ユーザの作成と権限付与
CREATE USER 'sqladmin'@'localhost' IDENTIFIED BY 'sqladmin';
GRANT ALL on *.* to sqladmin@localhost;

# データベースの作成
CREATE DATABASE IF NOT EXISTS lab_login_system_2;
USE lab_login_system_2;

# テーブルの作成
CREATE TABLE IF NOT EXISTS member (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    macaddr VARCHAR(255) NOT NULL,
    notionid VARCHAR(255) NOT NULL
);