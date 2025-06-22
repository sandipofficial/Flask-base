DROP DATABASE IF EXISTS epytododb;

CREATE DATABASE IF NOT EXISTS epytododb;

USE epytododb;

DROP TABLE IF EXISTS user;

CREATE TABLE IF NOT EXISTS user
(
    userid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    username VARCHAR(10) NOT NULL,
    `password` VARCHAR(18) NOT NULL
);

DROP TABLE IF EXISTS task;

CREATE TABLE IF NOT EXISTS task
(
    task_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    title VARCHAR(50) NOT NULL,
    content VARCHAR(50),
    `begin` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP(),
    `end` text,
    `status` INT(11) DEFAULT NULL
);

INSERT INTO `user` (`userid`, `username`, `password`) VALUES (1, 'test', 'test');

DROP TABLE IF EXISTS user_has_task;

CREATE TABLE IF NOT EXISTS user_has_task
(
    fk_user_id INT(11) NOT NULL,
    fk_task_id INT(11) NOT NULL
);