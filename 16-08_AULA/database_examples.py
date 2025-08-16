# Exemplo 1: Usando SQLite (banco de dados embutido no Python)
import sqlite3

# Passo 1: Conectar ao banco de dados SQLite
# Se o arquivo 'escola.db' não existir, ele será criado automaticamente
conn_sqlite = sqlite3.connect('escola.db')
cursor_sqlite = conn_sqlite.cursor()

# Passo 2: Criar uma tabela para armazenar alunos
cursor_sqlite.execute('''
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER,
        curso TEXT
    )
''')

# Passo 3: Inserir dados (CREATE)
cursor_sqlite.execute("INSERT INTO alunos (nome, idade, curso) VALUES (?, ?, ?)", 
                     ("João Silva", 20, "Ciência da Computação"))
cursor_sqlite.execute("INSERT INTO alunos (nome, idade, curso) VALUES (?, ?, ?)", 
                     ("Maria Oliveira", 19, "Engenharia"))

# Passo 4: Commit para salvar as alterações
conn_sqlite.commit()

# Passo 5: Consultar dados (READ)
cursor_sqlite.execute("SELECT * FROM alunos")
alunos = cursor_sqlite.fetchall()
print("Dados no SQLite:")
for aluno in alunos:
    print(f"ID: {aluno[0]}, Nome: {aluno[1]}, Idade: {aluno[2]}, Curso: {aluno[3]}")

# Passo 6: Atualizar dados (UPDATE)
cursor_sqlite.execute("UPDATE alunos SET idade = ? WHERE nome = ?", (21, "João Silva"))
conn_sqlite.commit()

# Passo 7: Deletar dados (DELETE)
cursor_sqlite.execute("DELETE FROM alunos WHERE nome = ?", ("Maria Oliveira",))
conn_sqlite.commit()

# Passo 8: Fechar a conexão
conn_sqlite.close()

# Exemplo 2: Usando MySQL (necessita do pacote mysql-connector-python)
import mysql.connector

# Passo 1: Conectar ao banco de dados MySQL
# Substitua 'seu_usuario', 'sua_senha' e 'seu_host' pelos valores reais
conn_mysql = mysql.connector.connect(
    host="seu_host",
    user="seu_usuario",
    password="sua_senha",
    database="escola"
)
cursor_mysql = conn_mysql.cursor()

# Passo 2: Criar uma tabela para armazenar alunos
cursor_mysql.execute('''
    CREATE TABLE IF NOT EXISTS alunos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        idade INT,
        curso VARCHAR(255)
    )
''')

# Passo 3: Inserir dados (CREATE)
sql_insert = "INSERT INTO alunos (nome, idade, curso) VALUES (%s, %s, %s)"
valores = ("Ana Costa", 22, "Matemática")
cursor_mysql.execute(sql_insert, valores)
conn_mysql.commit()

# Passo 4: Consultar dados (READ)
cursor_mysql.execute("SELECT * FROM alunos")
alunos_mysql = cursor_mysql.fetchall()
print("\nDados no MySQL:")
for aluno in alunos_mysql:
    print(f"ID: {aluno[0]}, Nome: {aluno[1]}, Idade: {aluno[2]}, Curso: {aluno[3]}")

# Passo 5: Atualizar dados (UPDATE)
cursor_mysql.execute("UPDATE alunos SET curso = %s WHERE nome = %s", 
                    ("Física", "Ana Costa"))
conn_mysql.commit()

# Passo 6: Deletar dados (DELETE)
cursor_mysql.execute("DELETE FROM alunos WHERE nome = %s", ("Ana Costa",))
conn_mysql.commit()

# Passo 7: Fechar a conexão
cursor_mysql.close()
conn_mysql.close()