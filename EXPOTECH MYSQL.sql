/*create database GameTree;*/
use GameTree;

/*
CREATE TABLE IF NOT EXISTS usuarios (
	id_usuario INT AUTO_INCREMENT PRIMARY KEY,
	nome_usuario VARCHAR(100) NOT NULL UNIQUE,
	email VARCHAR(255) NOT NULL,
	senha VARCHAR(255) NOT NULL,
	nivel INT DEFAULT 1
    );
    
CREATE TABLE IF NOT EXISTS jogos (
	id_jogo INT AUTO_INCREMENT PRIMARY KEY,
	titulo VARCHAR(150) NOT NULL UNIQUE,
	descricao TEXT NOT NULL,
	link_steam VARCHAR(255) NOT NULL,
	ram_minima INT NOT NULL,
	armazenamento_minimo INT NOT NULL,
	cpu_minima VARCHAR(150) NOT NULL,
	gpu_minima VARCHAR(150) NOT NULL
);

CREATE TABLE IF NOT EXISTS comentarios (
	id_comentario INT AUTO_INCREMENT PRIMARY KEY,
	id_jogo INT NOT NULL,
	nome_usuario VARCHAR(100) NOT NULL,
	texto TEXT NOT NULL,
	estrelas INT NOT NULL,
	recomenda CHAR(1) NOT NULL,
	data_postagem DATETIME DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (id_jogo) REFERENCES jogos (id_jogo) ON DELETE CASCADE
);*/

