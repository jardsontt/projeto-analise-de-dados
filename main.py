import pandas as pd
import datetime
import random
import sqlite3

#criando os dados da tabela projetos
projetos = []
for i in range(1, 1001):
    nome = f"Projeto {i}"
    descricao = f"Descrição do Projeto {i}"
    data_inicio = datetime.date(random.randint(2020, 2023), random.randint(1, 12), random.randint(1, 28))
    data_termino = data_inicio + datetime.timedelta(days=random.randint(30, 365))
    projetos.append((nome, descricao, str(data_inicio), str(data_termino)))

#cria os departamentos
departamentos = ["Desenvolvimento", "Marketing", "RH", "Financeiro", "Vendas"]

#cria os funcionarios
funcionarios = []
cargos = ["Analista", "Gerente", "Desenvolvedor", "Estagiário", "Coordenador"]
for i in range(1, 2001):
    nome = f"Funcionário {i}"
    cargo = random.choice(cargos)
    departamento = random.choice(departamentos)
    funcionarios.append((nome, cargo, departamento))

#cria as tarefas
tarefas = []
status = ["Pendente", "Em Andamento", "Concluída"]
tarefa_id = 1

for projeto_id in range(1, 1001):
    num_tarefas = random.randint(5, 20)
    for _ in range(num_tarefas):
        nome = f"Tarefa {tarefa_id}"
        descricao = f"Descrição da Tarefa {tarefa_id}"
        status_tarefa = random.choice(status)
        tarefas.append((projeto_id, nome, descricao, status_tarefa))
        tarefa_id += 1

#gera atribuicoes (3 por funcionario)
atribuicoes = []
tarefa_ids = [tarefa[0] for tarefa in tarefas]  # Lista de IDs de tarefas
for funcionario_id in range(1, 5001):
    tarefas_atribuidas = random.sample(tarefa_ids, 2)  # Seleciona 3 tarefas aleatórias
    for tarefa_id in tarefas_atribuidas:
        data_atribuicao = datetime.date(random.randint(2022, 2023), random.randint(1, 12), random.randint(1, 28))
        atribuicoes.append((funcionario_id, tarefa_id, str(data_atribuicao)))

def cria_bando_de_dados():
  conn = sqlite3.connect('projetos.db')
  cursor  = conn.cursor()

  cursor.execute('''
    CREATE TABLE IF NOT EXISTS projetos(
      id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
      nome VARCHAR UNIQUE NOT NULL,
      descricao VARCHAR NOT NULL,
      data_inicio DATE NOT NULL,
      data_termino DATE
    )
  ''')
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS tarefas(
      id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
      projeto_id INTEGER NOT NULL,
      nome VARCHAR NOT NULL,
      descricao VARCHAR NOT NULL,
      status VARCHAR NOT NULL
      )
  ''')
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS funcionarios(
      id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
      nome VARCHAR NOT NULL,
      cargo VARCHAR NOT NULL,
      departamento VARCHAR NOT NULL
    )
  ''')
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS atribuicoes(
      id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
      funcionario_id INTEGER NOT NULL,
      tarefa_id INTEGER NOT NULL,
      data_atribuicao DATE NOT NULL
    )
  ''')
  conn.commit()
  conn.close()
cria_bando_de_dados()

def limpa_banco_de_dados():
  conn = conecta_banco_de_dados()
  if conn:
    cursor = conn.cursor()
    try:
      cursor.execute('DELETE FROM atribuicoes')
      cursor.execute('DELETE FROM tarefas')
      cursor.execute('DELETE FROM funcionarios')
      cursor.execute('DELETE FROM projetos')
      conn.commit()
      print("Banco de dados limpo com sucesso!")
    finally:
      conn.close()
  else:
    print("Falha ao conectar ao banco de dados.")

def conecta_banco_de_dados():

  try:
    conn = sqlite3.connect('projetos.db')
    return conn
  except sqlite3.Error as e:
    print(f"Erro ao conectar ao banco de dados: {e}")
    return None

def insere_projetos(projetos):
  conn = conecta_banco_de_dados()
  if conn:
    cursor = conn.cursor()
    try:
      # Insert projects one by one to reduce the lock duration
      for projeto in projetos:
        try:
            cursor.execute('''
              INSERT INTO projetos (nome, descricao, data_inicio, data_termino)
              VALUES (?, ?, ?, ?)
            ''', projeto)
        except sqlite3.IntegrityError:
            print(f"Projeto com nome '{projeto[0]}' já existe. Ignorando.")
      conn.commit()  # Commit after all insertions
      print("Projetos inseridos com sucesso!")
    finally:
      conn.close()
  else:
    print("Falha ao conectar ao banco de dados.")
insere_projetos(projetos)

def insere_tarefas(tarefas):
  conn = conecta_banco_de_dados()
  if conn:
    cursor = conn.cursor()
    try:
      for tarefa in tarefas:
        try:
          cursor.execute('INSERT INTO tarefas (projeto_id, nome, descricao, status) VALUES (?, ?, ?, ?)', tarefa)
        except sqlite3.Error as e:
          print(f"Erro ao inserir tarefas: {e}")
      conn.commit()
      print("Tarefas inseridas com sucesso!")
    finally:
        conn.close()
  else:
    print("Falha ao conectar ao banco de dados.")
insere_tarefas(tarefas)

def insere_funcionarios(funcionarios):
  conn = conecta_banco_de_dados()
  if conn:
    cursor = conn.cursor()
    try:
      for funcionario in funcionarios:
        try:
          cursor.execute('INSERT INTO funcionarios (nome, cargo, departamento) VALUES (?, ?, ?)', funcionario)
        except sqlite3.Error as e:
          print(f"Erro ao inserir funcionarios: {e}")
      conn.commit()
      print("Funcionarios inseridos com sucesso!")
    finally:
      conn.close()
  else:
    print("Falha ao conectar ao banco de dados.")
insere_funcionarios(funcionarios)

def insere_atribuicoes(atribuicoes):
  conn = conecta_banco_de_dados()
  if conn:
    cursor = conn.cursor()
    try:
      for atribuicao in atribuicoes:
        try:
          cursor.execute('INSERT INTO atribuicoes (funcionario_id, tarefa_id, data_atribuicao) VALUES (?, ?, ?)', atribuicao)
        except sqlite3.Error as e:
          print(f"Erro ao inserir atribuicoes: {e}")
      conn.commit()
      print("Atribuicoes inseridas com sucesso!")
    finally:
      conn.close()
  else:
    print("Falha ao conectar ao banco de dados")
insere_atribuicoes(atribuicoes)

def executa_consulta(conn, consulta, parametros=()):
    try:
        cursor = conn.cursor()
        cursor.execute(consulta,parametros)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro na consulta SQL: {e}")
        return []
def tarefas_concluidas(projeto):
    conn = conecta_banco_de_dados()
    if conn:
        consulta = ('''
            SELECT COUNT(*)
            FROM Tarefas
            JOIN Projetos ON Tarefas.projeto_id = Projetos.id
            WHERE Projetos.nome = ? AND Tarefas.status = 'Concluída';
            ''')
        resultados = executa_consulta(conn, consulta, (projeto,))
        conn.close()
        return [resultado[0] for resultado in resultados]
    else:
        print("Não foi possivel se conectar ao banco de dados!")
        return None

numero = input("insira o numero do projeto: ")
print('Numero de tarefas concluidas: ', tarefas_concluidas(f'Projeto {int(numero)}'))

limpa_banco_de_dados()
# mais features a serem adicionadas