-- ===============================
-- POPULAÇÃO INICIAL DO BANCO QUIZ_DS_INFOR
-- ===============================

-- Seleciona o banco
USE quiz_ds_infor;

-- ===============================
-- INSERÇÃO DE DADOS INICIAIS
-- ===============================

-- --- TEMAS ---
INSERT INTO temas (nome)
VALUES
    ('Lógica de Programação'),
    ('Banco de Dados'),
    ('Redes de Computadores'),
    ('Desenvolvimento Web'),
    ('Hardware e Sistemas Operacionais')
ON DUPLICATE KEY UPDATE nome = VALUES(nome);

-- --- NÍVEIS DE DIFICULDADE ---
INSERT INTO niveis_dificuldade (nome, nivel_dificuldade)
VALUES
    ('Fácil', 1),
    ('Médio', 2),
    ('Difícil', 3)
ON DUPLICATE KEY UPDATE nome = VALUES(nome);

-- --- EXPLICAÇÕES DAS RESPOSTAS ---
INSERT INTO explicacoes_respostas (conteudo)
VALUES
    (
        JSON_OBJECT(
            'titulo', 'Estrutura condicional',
            'texto', 'A estrutura condicional "if" permite executar um bloco de código apenas se uma condição for verdadeira.'
        )
    ),
    (
        JSON_OBJECT(
            'titulo', 'Chave primária',
            'texto', 'A chave primária identifica unicamente cada registro em uma tabela, garantindo integridade referencial.'
        )
    ),
    (
        JSON_OBJECT(
            'titulo', 'Modelo OSI',
            'texto', 'O modelo OSI possui 7 camadas que padronizam a comunicação entre sistemas de rede.'
        )
    ),
    (
        JSON_OBJECT(
            'titulo', 'Integração entre front-end e banco de dados',
            'texto', 'Em uma aplicação web, o back-end atua como intermediário entre o front-end e o banco de dados, processando requisições e retornando dados.'
        )
    );

-- --- PERGUNTAS ---
INSERT INTO perguntas (conteudo, alternativas, id_resposta, id_explicacao, id_tema, id_nivel)
VALUES
    (
        JSON_OBJECT('pergunta', 'Qual estrutura de controle é usada para decidir entre duas ou mais ações em programação?'),
        JSON_ARRAY('Loop for', 'If-else', 'Switch', 'Função'),
        2,  -- resposta correta: "If-else"
        1,  -- explicação correspondente
        1,  -- tema: Lógica de Programação
        1   -- nível: Fácil
    ),
    (
        JSON_OBJECT('pergunta', 'Qual é o principal objetivo de uma chave primária em uma tabela de banco de dados?'),
        JSON_ARRAY('Permitir duplicação de registros', 'Aumentar desempenho de consultas', 'Identificar unicamente cada linha', 'Controlar permissões de acesso'),
        3,  -- resposta correta: "Identificar unicamente cada linha"
        2,  -- explicação correspondente
        2,  -- tema: Banco de Dados
        2   -- nível: Médio
    ),
    (
        JSON_OBJECT('pergunta', 'Quantas camadas existem no modelo OSI de redes?'),
        JSON_ARRAY('3', '5', '7', '9'),
        3,  -- resposta correta: "7"
        3,  -- explicação correspondente
        3,  -- tema: Redes de Computadores
        1   -- nível: Fácil
    ),
    (
        JSON_OBJECT('pergunta', 'Qual tecnologia conecta o front-end ao banco de dados em uma aplicação web completa?'),
        JSON_ARRAY('CSS', 'JavaScript', 'Back-end', 'HTML'),
        3,  -- resposta correta: "Back-end"
        4,  -- explicação correspondente
        4,  -- tema principal: Desenvolvimento Web
        2   -- nível: Médio
    );

-- --- PERGUNTAS_TEMAS ---
-- Inclui a pergunta 4 em dois temas: Desenvolvimento Web e Banco de Dados
INSERT INTO perguntas_temas (id_pergunta, id_tema)
VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),  -- Desenvolvimento Web
    (4, 2)   -- Banco de Dados (tema adicional)
ON DUPLICATE KEY UPDATE id_tema = VALUES(id_tema);
