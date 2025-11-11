CREATE DATABASE IF NOT EXISTS quiz_ds_infor
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;

-- Cria o banco de dados do quiz
CREATE database quiz_ds_infor;

-- Define o banco de dados do quiz como o
-- banco de dados padrão para a sessão atual
USE quiz_ds_infor;

-- ----- Cria as Tabelas -----

-- --- Temas ---
CREATE table temas(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- --- Níveis de Dificuldade ---
CREATE table niveis_dificuldade(
	id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(20) NOT NULL,
    nivel_dificuldade TINYINT NOT NULL
);

-- --- Explicações das Respostas ---
CREATE table explicacoes_respostas(
    id INT AUTO_INCREMENT PRIMARY KEY,
    conteudo JSON NOT NULL
);

-- --- Perguntas ---
CREATE table perguntas(
	id INT AUTO_INCREMENT PRIMARY KEY,
    conteudo JSON NOT NULL,
    alternativas JSON NOT NULL,
    id_resposta INT NOT NULL,
    -- Explicação, Tema e Nível de Dificuldade
    id_explicacao INT,
    id_tema INT,
    id_nivel INT,
    FOREIGN KEY (id_explicacao) REFERENCES explicacoes_respostas(id),
    FOREIGN KEY (id_tema) REFERENCES temas(id),
    FOREIGN KEY (id_nivel) REFERENCES niveis_dificuldade(id)
);

-- --- Perguntas e Temas ---
CREATE TABLE perguntas_temas (
    id_pergunta INT,
    id_tema INT,
    FOREIGN KEY (id_pergunta) REFERENCES perguntas(id),
    FOREIGN KEY (id_tema) REFERENCES temas(id),
    PRIMARY KEY (id_pergunta, id_tema)
);
