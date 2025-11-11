from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
import json


app = Flask(__name__)

HOST = "0.0.0.0"
PORT = 5000
DB_NAME = "quiz_ds_infor"

caminho_schema_sql = "schema.sql"
caminho_population_sql = "population.sql"

alfabeto_minusculo = [chr(i) for i in range(ord("a"), ord("z") + 1)]
alfabeto_maiusculo = [chr(i) for i in range(ord("A"), ord("Z") + 1)]


# Define o diretório de trabalho como o diretório do arquivo Python
caminho_script = os.path.dirname(os.path.abspath(__file__))
os.chdir(caminho_script)


# ----- Auxiliares -----


def limpar_terminal(aguardar: bool = False):
    """
    Limpa o terminal.
    Se aguardar=True, o terminal só limpa depois do usuário pressionar ENTER.
    """

    if aguardar:
        input("\nPressione ENTER para continuar...")

    # Windows usa "cls", Linux/mac usa "clear"
    os.system("cls" if os.name == "nt" else "clear")


# ----- Banco de Dados -----


def executar_sql(caminho_sql: str):
    conexao = mysql.connector.connect(
        host="localhost", user="root", password="", autocommit=False
    )
    cursor = conexao.cursor()

    with open(caminho_sql, "r", encoding="utf-8") as file:
        linhas = file.readlines()

    comando_atual = []
    dentro_comentario = False

    for num_linha, linha in enumerate(linhas, start=1):
        linha_strip = linha.strip()

        # Detecta início/fim de comentário multilinha
        if linha_strip.startswith("/*"):
            dentro_comentario = True
            continue
        if dentro_comentario:
            if "*/" in linha_strip:
                dentro_comentario = False
            continue

        # Ignora linhas de comentário simples
        if linha_strip.startswith("--") or not linha_strip:
            continue

        # Acumula linha atual
        comando_atual.append(linha)

        # Se encontrou o fim de comando
        if linha_strip.endswith(";"):
            comando_sql = "".join(comando_atual).strip()

            try:
                cursor.execute(comando_sql)
            except Exception as e:
                print(f"\n⚠️ Erro na linha {num_linha}: {e}")
                print(f"Comando problemático:\n{comando_sql}\n")
            comando_atual = []  # limpa o buffer

    conexao.commit()
    cursor.close()
    conexao.close()


def inicializar_banco_de_dados():
    executar_sql(caminho_schema_sql)


def conectar():
    conexao = mysql.connector.connect(
        host="localhost", user="root", password="", database=DB_NAME
    )
    return conexao


# ----- CRUD -----

"""
# --- Criar ---
def adicionar_livro(titulo: str, autor: str, ano_publicacao: int, src_imagem: str):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    sql = f"INSERT INTO livros(titulo, autor, ano_publicacao, src_imagem) VALUES (%s, %s, %s, %s)"
    valores = (titulo, autor, ano_publicacao, src_imagem)

    cursor.execute(sql, valores)
    conexao.commit()
    conexao.close()

    print("Livro Adicionado com Sucesso!!!")
"""


# --- Ler/Listar ---
# - Perguntas -
def listar_perguntas():
    conexao = mysql.connector.connect(
        host="localhost", user="root", password="", database=DB_NAME
    )
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM perguntas")
    perguntas = cursor.fetchall()
    conexao.close()

    # Converte JSONs para dict/list
    for p in perguntas:
        p["conteudo"] = json.loads(p["conteudo"])
        p["alternativas"] = json.loads(p["alternativas"])

    return perguntas


# - ID dos Temas através do ID da Pergunta -
def listar_ids_temas_pelo_id_pergunta(id_pergunta: int):
    conexao = mysql.connector.connect(
        host="localhost", user="root", password="", database=DB_NAME
    )
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            p.id AS id_pergunta,
            t.id AS id_tema
        FROM
            perguntas AS p
        INNER JOIN
            perguntas_temas AS pt ON p.id = pt.id_pergunta
        INNER JOIN
            temas AS t ON pt.id_tema = t.id
        WHERE
            p.id = %s;
    """,
        (id_pergunta,),
    )

    resultados = cursor.fetchall()
    conexao.close()

    lista_ids_temas = {linha["id_tema"] for linha in resultados}

    return lista_ids_temas


# - Nomes dos Temas através do ID da Pergunta -
def listar_nomes_temas_pelo_id_pergunta(id_pergunta: int):
    conexao = mysql.connector.connect(
        host="localhost", user="root", password="", database=DB_NAME
    )
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            p.id AS id_pergunta,
            t.id AS id_tema,
            t.nome AS nome_tema
        FROM
            perguntas AS p
        INNER JOIN
            perguntas_temas AS pt ON p.id = pt.id_pergunta
        INNER JOIN
            temas AS t ON pt.id_tema = t.id
        WHERE
            p.id = %s;
    """,
        (id_pergunta,),
    )

    resultados = cursor.fetchall()
    conexao.close()

    lista_nomes_temas = [linha["nome_tema"] for linha in resultados]

    return lista_nomes_temas


'''
# --- Atualizar ---
def atualizar_livros(id_livro, novo_titulo, novo_autor, novo_ano):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    sql = """
    UPDATE livros
    SET titulo = %s, autor = %s, ano_publicacao = %s
    WHERE id = %s
    """
    valores = (novo_titulo, novo_autor, novo_ano, id_livro)

    cursor.execute(sql, valores)
    conexao.commit()
    conexao.close()


# --- Excluir ---
def excluir_livro(id_livro):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("DELETE FROM livros WHERE id = %s", (id_livro,))
    conexao.commit()
    conexao.close()

    print("Livro Excluído com Sucesso!!!")
'''


def popular_db():
    conexao = mysql.connector.connect(
        host="localhost", user="root", password="", database=DB_NAME
    )
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM perguntas;")
    resultado = cursor.fetchone()
    conexao.close()

    if resultado["total"] == 0:
        print("📥 Populando banco de dados...")
        executar_sql(caminho_population_sql)
    else:
        print("✅ Banco já populado. Nenhuma ação necessária.")


# ----- Rotas -----
# --- Páginas ---
# Ler/Listar
@app.route("/")
def index():
    # Faz uma requisição por todas as perguntas
    perguntas = listar_perguntas()

    return render_template("index.html", perguntas=perguntas)


# Quiz
@app.route("/quiz.html")
def quiz():
    # Faz uma requisição por todas as perguntas
    perguntas = listar_perguntas()
    # Pega os nomes dos temas e correlaciona com o ID
    nomes_temas = {}
    for pergunta in perguntas:
        id = pergunta["id"]
        nomes_temas[id] = listar_nomes_temas_pelo_id_pergunta(id)
    indicadores_alternativas = alfabeto_minusculo

    return render_template(
        "quiz.html",
        perguntas=perguntas,
        nomes_temas=nomes_temas,
        indicadores_alternativas=indicadores_alternativas,
    )


'''
# Criar
@app.route("/adicionar.html")
def adicionar_html():

    # Faz uma requisição por todos os bimestres
    bimestres = query_db(
        """
        SELECT 
            bimestres.id_bimestre, 
            bimestres.nome
        FROM bimestres
        ORDER BY bimestres.nome;"""
    )

    # Faz uma requisição por todas as disciplinas
    disciplinas = query_db(
        """
        SELECT 
            disciplinas.id_disciplina, 
            disciplinas.nome
        FROM disciplinas
        ORDER BY disciplinas.nome;"""
    )

    # Faz uma requisição por todas as salas
    salas = query_db(
        """
        SELECT 
            salas.id_sala, 
            salas.nome
        FROM salas
        ORDER BY salas.nome;"""
    )

    # Faz uma requisição por todas as notas
    notas = query_db(
        """
        SELECT 
            notas.id_nota, 
            notas.valor, 
            -- Cria aliases
            alunos.nome AS nome_aluno,
            disciplinas.nome AS nome_disciplina,
            bimestres.nome AS nome_bimestre
        FROM notas
        -- Une notas.id_aluno, notas.id_disciplina e notas.id_bimestre
        JOIN alunos ON notas.id_aluno = alunos.id_aluno
        JOIN disciplinas ON notas.id_disciplina = disciplinas.id_disciplina
        JOIN bimestres ON notas.id_bimestre = bimestres.id_bimestre
        ORDER BY notas.id_nota;"""
    )

    return render_template(
        "adicionar.html",
        bimestres=bimestres,
        disciplinas=disciplinas,
        salas=salas,
        notas=notas,
    )


# Excluir
@app.route("/excluir.html")
def excluir_html():
    # Faz uma requisição por todos os bimestres
    bimestres = query_db(
        """
        SELECT 
            bimestres.id_bimestre, 
            bimestres.nome
        FROM bimestres
        ORDER BY bimestres.nome;"""
    )

    # Faz uma requisição por todas as disciplinas
    disciplinas = query_db(
        """
        SELECT 
            disciplinas.id_disciplina, 
            disciplinas.nome
        FROM disciplinas
        ORDER BY disciplinas.nome;"""
    )

    # Faz uma requisição por todas as salas
    salas = query_db(
        """
        SELECT 
            salas.id_sala, 
            salas.nome
        FROM salas
        ORDER BY salas.nome;"""
    )

    # Faz uma requisição por todos os alunos
    alunos = query_db(
        """
        SELECT 
            alunos.id_aluno, 
            alunos.nome, 
            salas.nome AS nome_sala -- Cria um alias
        FROM alunos
        -- Une alunos.id_sala a salas.id_sala
        JOIN salas ON alunos.id_sala = salas.id_sala
        ORDER BY salas.nome;"""
    )

    # Faz uma requisição por todas as notas
    notas = query_db(
        """
        SELECT 
            notas.id_nota, 
            notas.valor, 
            -- Cria aliases
            alunos.nome AS nome_aluno,
            disciplinas.nome AS nome_disciplina,
            bimestres.nome AS nome_bimestre
        FROM notas
        -- Une notas.id_aluno, notas.id_disciplina e notas.id_bimestre
        JOIN alunos ON notas.id_aluno = alunos.id_aluno
        JOIN disciplinas ON notas.id_disciplina = disciplinas.id_disciplina
        JOIN bimestres ON notas.id_bimestre = bimestres.id_bimestre
        ORDER BY alunos.nome;"""
    )

    return render_template(
        "excluir.html",
        bimestres=bimestres,
        disciplinas=disciplinas,
        salas=salas,
        alunos=alunos,
        notas=notas,
    )


# Atualizar
@app.route("/atualizar.html")
def atualizar_html():

    # Faz uma requisição por todos os bimestres
    bimestres = query_db(
        """
        SELECT 
            bimestres.id_bimestre, 
            bimestres.nome
        FROM bimestres
        ORDER BY bimestres.nome;"""
    )

    # Faz uma requisição por todas as disciplinas
    disciplinas = query_db(
        """
        SELECT 
            disciplinas.id_disciplina, 
            disciplinas.nome
        FROM disciplinas
        ORDER BY disciplinas.nome;"""
    )

    # Faz uma requisição por todas as salas
    salas = query_db(
        """
        SELECT 
            salas.id_sala, 
            salas.nome
        FROM salas
        ORDER BY salas.nome;"""
    )

    # Faz uma requisição por todos os alunos
    alunos = query_db(
        """
        SELECT 
            alunos.id_aluno, 
            alunos.nome, 
            salas.nome AS nome_sala -- Cria um alias
        FROM alunos
        -- Une alunos.id_sala a salas.id_sala
        JOIN salas ON alunos.id_sala = salas.id_sala
        ORDER BY salas.nome;"""
    )

    # Faz uma requisição por todas as notas
    notas = query_db(
        """
        SELECT 
            notas.id_nota, 
            notas.valor, 
            -- Cria aliases
            alunos.nome AS nome_aluno,
            disciplinas.nome AS nome_disciplina,
            bimestres.nome AS nome_bimestre
        FROM notas
        -- Une notas.id_aluno, notas.id_disciplina e notas.id_bimestre
        JOIN alunos ON notas.id_aluno = alunos.id_aluno
        JOIN disciplinas ON notas.id_disciplina = disciplinas.id_disciplina
        JOIN bimestres ON notas.id_bimestre = bimestres.id_bimestre
        ORDER BY alunos.nome;"""
    )

    return render_template(
        "atualizar.html",
        bimestres=bimestres,
        disciplinas=disciplinas,
        salas=salas,
        alunos=alunos,
        notas=notas,
    )
'''


if __name__ == "__main__":
    with app.app_context():
        limpar_terminal()
        print("----- Inicializando Banco de Dados -----")
        inicializar_banco_de_dados()
        print("----- Populando Banco de Dados -----")
        popular_db()
    app.run(host=HOST, port=PORT, debug=True)
