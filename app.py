from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os


app = Flask(__name__)
HOST = "0.0.0.0"
PORT = 5000
caminho_schema_sql = "schema.sql"
caminho_population_sql = "population.sql"


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
    comando_atual = ""
    comentario_multilinha = False

    # Conecta-se ao banco de dados
    print("--- Conecta-se ao banco de dados ---")
    conexao = mysql.connector.connect(host="localhost", user="root", password="")
    cursor = conexao.cursor(dictionary=True)

    # Lê o schema.sql
    with open(caminho_sql, "r") as file:
        linhas = file.readlines()
        file.close()

    for linha in linhas:
        # Fim de um Comentário Multilinha
        if comentario_multilinha == True and "*/" in linha:
            comentario_multilinha = False
        # Ainda dentro de um comentário multilinha
        elif comentario_multilinha == True:
            continue
        # Começo de um Comentário Multilinha
        elif linha.startswith("/*"):
            comentario_multilinha = True
        # Comentário de linha única
        elif "-- " in linha:
            antes, _, depois = linha.partition("--")
            print(_ + depois)
            cursor.execute(antes)
        # Fim de um comando
        elif linha.endswith(";") or linha.endswith(";\n"):
            comando_atual += linha
            # Tenda executar
            try:
                cursor.execute(comando_atual)
            # Mostra o erro
            except Exception as e:
                print(e)
            comando_atual = ""
        # Acrescenta as linhas ao comando atual
        else:
            comando_atual += linha

    conexao.commit()
    conexao.close()


def inicializar_banco_de_dados():
    executar_sql(caminho_schema_sql)


def conectar():
    conexao = mysql.connector.connect(
        host="localhost", user="root", password="", database="biblioteca_python"
    )
    return conexao


# ----- CRUD -----


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


# --- Ler/Listar ---
def listar_livros():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT * from livros")
    livros = cursor.fetchall()  # Pega todos os resultados
    conexao.close()

    if livros:
        print("Livro encontrado!")
    else:
        print("Nenhum livro encontrado!")

    return livros


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


def popular_db():
    executar_sql(caminho_population_sql)


# ----- Rotas -----
# --- Páginas ---
# Ler/Listar
@app.route("/")
def index():
    # Faz uma requisição por todos os livros
    livros = listar_livros()

    return render_template("index.html", livros=livros)


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


if __name__ == "__main__":
    with app.app_context():
        limpar_terminal()
        print("----- Inicializando Banco de Dados -----")
        inicializar_banco_de_dados()
        print("----- Populando Banco de Dados -----")
        popular_db()
    app.run(host=HOST, port=PORT, debug=True)
