-- Usa o banco criado
USE quiz_ds_infor;

-- ----- INSERE DADOS INICIAIS -----

-- --- Temas ---
INSERT INTO temas (nome) VALUES
('Lógica de Programação'),
('Banco de Dados'),
('Redes de Computadores'),
('Desenvolvimento Web'),
('Hardware e Sistemas Operacionais');

-- --- Níveis de Dificuldade ---
INSERT INTO niveis_dificuldade (nome, nivel_dificuldade) VALUES
('Fácil', 1),
('Médio', 2),
('Difícil', 3);

-- --- Explicações das Respostas ---
INSERT INTO explicacoes_respostas (conteudo) VALUES
(JSON_OBJECT(
    'titulo', 'Estrutura condicional',
    'texto', 'A estrutura condicional "if" permite executar um bloco de código apenas se uma condição for verdadeira.'
)),
(JSON_OBJECT(
    'titulo', 'Chave primária',
    'texto', 'A chave primária identifica unicamente cada registro em uma tabela, garantindo integridade referencial.'
)),
(JSON_OBJECT(
    'titulo', 'Modelo OSI',
    'texto', 'O modelo OSI possui 7 camadas que padronizam a comunicação entre sistemas de rede.'
));

-- --- Perguntas ---
INSERT INTO perguntas (conteudo, alternativas, id_resposta, id_explicacao, id_tema, id_nivel)
VALUES
(
    JSON_OBJECT('pergunta', 'Qual estrutura de controle é usada para decidir entre duas ou mais ações em programação?'),
    JSON_ARRAY('Loop for', 'If-else', 'Switch', 'Função'),
    2,
    1,
    1,
    1
),
(
    JSON_OBJECT('pergunta', 'Qual é o principal objetivo de uma chave primária em uma tabela de banco de dados?'),
    JSON_ARRAY('Permitir duplicação de registros', 'Aumentar desempenho de consultas', 'Identificar unicamente cada linha', 'Controlar permissões de acesso'),
    3,
    2,
    2,
    2
),
(
    JSON_OBJECT('pergunta', 'Quantas camadas existem no modelo OSI de redes?'),
    JSON_ARRAY('3', '5', '7', '9'),
    3,
    3,
    3,
    1
);

-- --- Perguntas e Temas ---
INSERT INTO perguntas_temas (id_pergunta, id_tema) VALUES
(1, 1),
(2, 2),
(3, 3);
