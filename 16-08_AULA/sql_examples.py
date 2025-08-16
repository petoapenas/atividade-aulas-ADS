import sqlite3

# Passo 1: Conectar ao banco de dados SQLite
conn = sqlite3.connect('escola_avancada.db')
cursor = conn.cursor()

# Passo 2: Criar tabelas para alunos e disciplinas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER,
        curso TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS disciplinas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_disciplina TEXT NOT NULL,
        aluno_id INTEGER,
        nota REAL,
        FOREIGN KEY (aluno_id) REFERENCES alunos(id)
    )
''')

# Passo 3: Inserir dados em alunos
cursor.executemany("INSERT INTO alunos (nome, idade, curso) VALUES (?, ?, ?)", [
    ("João Silva", 20, "Ciência da Computação"),
    ("Maria Oliveira", 19, "Engenharia"),
    ("Pedro Santos", 21, "Matemática")
])
conn.commit()

# Passo 4: Inserir dados em disciplinas
cursor.executemany("INSERT INTO disciplinas (nome_disciplina, aluno_id, nota) VALUES (?, ?, ?)", [
    ("Programação", 1, 8.5),
    ("Cálculo", 1, 7.0),
    ("Álgebra", 2, 9.0),
    ("Física", 2, 6.5),
    ("Estatística", 3, 8.0)
])
conn.commit()

# Exemplo 1: SELECT com WHERE e ORDER BY
# Objetivo: Selecionar alunos com idade maior que 19, ordenados por nome
cursor.execute("SELECT nome, idade, curso FROM alunos WHERE idade > 19 ORDER BY nome")
result = cursor.fetchall()
print("Exemplo 1 - Alunos com idade > 19, ordenados por nome:")
for row in result:
    print(f"Nome: {row[0]}, Idade: {row[1]}, Curso: {row[2]}")

# Exemplo 2: JOIN para combinar tabelas
# Objetivo: Listar alunos e suas disciplinas
cursor.execute('''
    SELECT alunos.nome, disciplinas.nome_disciplina, disciplinas.nota
    FROM alunos
    INNER JOIN disciplinas ON alunos.id = disciplinas.aluno_id
''')
result = cursor.fetchall()
print("\nExemplo 2 - Alunos e suas disciplinas:")
for row in result:
    print(f"Aluno: {row[0]}, Disciplina: {row[1]}, Nota: {row[2]}")

# Exemplo 3: Funções agregadas (COUNT, AVG, MIN, MAX)
# Objetivo: Contar disciplinas por aluno e calcular média, mínimo e máximo de notas
cursor.execute('''
    SELECT alunos.nome, 
           COUNT(disciplinas.id) as total_disciplinas, 
           AVG(disciplinas.nota) as media_notas,
           MIN(disciplinas.nota) as menor_nota,
           MAX(disciplinas.nota) as maior_nota
    FROM alunos
    LEFT JOIN disciplinas ON alunos.id = disciplinas.aluno_id
    GROUP BY alunos.nome
''')
result = cursor.fetchall()
print("\nExemplo 3 - Estatísticas por aluno:")
for row in result:
    print(f"Aluno: {row[0]}, Total Disciplinas: {row[1]}, Média: {row[2]:.2f}, Menor Nota: {row[3]}, Maior Nota: {row[4]}")

# Exemplo 4: UPDATE com condição
# Objetivo: Aumentar a nota de uma disciplina específica
cursor.execute("UPDATE disciplinas SET nota = nota + 1 WHERE nome_disciplina = ?", ("Programação",))
conn.commit()

# Exemplo 5: DELETE com condição
# Objetivo: Remover disciplinas com nota menor que 7.0
cursor.execute("DELETE FROM disciplinas WHERE nota < 7.0")
conn.commit()

# Exemplo 6: LIKE para busca parcial
# Objetivo: Buscar alunos com curso que contém "Ciência"
cursor.execute("SELECT nome, curso FROM alunos WHERE curso LIKE '%Ciência%'")
result = cursor.fetchall()
print("\nExemplo 6 - Alunos com curso contendo 'Ciência':")
for row in result:
    print(f"Nome: {row[0]}, Curso: {row[1]}")

# Passo 5: Fechar a conexão
conn.close()