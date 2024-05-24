create database dbms_project;
use dbms_project;

CREATE TABLE user (
  user_id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(255) NOT NULL,
  emailId VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  PRIMARY KEY (user_id)
);

CREATE TABLE website (
  webId INT NOT NULL AUTO_INCREMENT,
  website VARCHAR(255) NOT NULL,
  No_of_pass INT NOT NULL,
  PRIMARY KEY (webId)
);

CREATE TABLE password (
  password_id INT NOT NULL AUTO_INCREMENT,
  website VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  user_id INT NOT NULL,
  PRIMARY KEY (password_id),
  FOREIGN KEY (user_id) REFERENCES user(user_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE ip_address (
  user_id INT NOT NULL,
  Ip_Address VARCHAR(255) NOT NULL
);
