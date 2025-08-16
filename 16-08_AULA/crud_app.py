import sqlite3
from typing import List, Tuple

def conectar_banco() -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    """Conecta ao banco de dados SQLite e retorna a conexão e o cursor."""
    conn = sqlite3.connect('escola_crud.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER,
            curso TEXT
        )
    ''')
    return conn, cursor

def inserir_aluno(cursor: sqlite3.Cursor, conn: sqlite3.Connection, nome: str, idade: int, curso: str) -> None:
    """Insere um novo aluno no banco."""
    cursor.execute("INSERT INTO alunos (nome, idade, curso) VALUES (?, ?, ?)", (nome, idade, curso))
    conn.commit()
    print(f"Aluno '{nome}' inserido com sucesso!")

def listar_alunos(cursor: sqlite3.Cursor) -> List[Tuple]:
    """Lista todos os alunos."""
    cursor.execute("SELECT * FROM alunos")
    return cursor.fetchall()

def atualizar_aluno(cursor: sqlite3.Cursor, conn: sqlite3.Connection, id_aluno: int, nome: str, idade: int, curso: str) -> None:
    """Atualiza os dados de um aluno."""
    cursor.execute("UPDATE alunos SET nome = ?, idade = ?, curso = ? WHERE id = ?", (nome, idade, curso, id_aluno))
    if cursor.rowcount > 0:
        conn.commit()
        print(f"Aluno ID {id_aluno} atualizado com sucesso!")
    else:
        print(f"Aluno ID {id_aluno} não encontrado.")

def deletar_aluno(cursor: sqlite3.Cursor, conn: sqlite3.Connection, id_aluno: int) -> None:
    """Deleta um aluno pelo ID."""
    cursor.execute("DELETE FROM alunos WHERE id = ?", (id_aluno,))
    if cursor.rowcount > 0:
        conn.commit()
        print(f"Aluno ID {id_aluno} deletado com sucesso!")
    else:
        print(f"Aluno ID {id_aluno} não encontrado.")

def consultar_alunos(cursor: sqlite3.Cursor, campo: str, valor: str) -> List[Tuple]:
    """Consulta alunos com base em um campo e valor (usando LIKE)."""
    query = f"SELECT * FROM alunos WHERE {campo} LIKE ?"
    cursor.execute(query, (f"%{valor}%",))
    return cursor.fetchall()

def exibir_alunos(alunos: List[Tuple]) -> None:
    """Exibe a lista de alunos formatada."""
    if alunos:
        print("\nLista de Alunos:")
        for aluno in alunos:
            print(f"ID: {aluno[0]}, Nome: {aluno[1]}, Idade: {aluno[2]}, Curso: {aluno[3]}")
    else:
        print("Nenhum aluno encontrado.")

def main():
    conn, cursor = conectar_banco()
    
    while True:
        print("\n=== Sistema de Gerenciamento de Alunos ===")
        print("1. Inserir aluno")
        print("2. Listar todos os alunos")
        print("3. Atualizar aluno")
        print("4. Deletar aluno")
        print("5. Consultar alunos (por nome ou curso)")
        print("6. Sair")
        
        opcao = input("Escolha uma opção (1-6): ")
        
        if opcao == "1":
            nome = input("Digite o nome do aluno: ")
            try:
                idade = int(input("Digite a idade do aluno: "))
                curso = input("Digite o curso do aluno: ")
                inserir_aluno(cursor, conn, nome, idade, curso)
            except ValueError:
                print("Idade deve ser um número inteiro!")
                
        elif opcao == "2":
            alunos = listar_alunos(cursor)
            exibir_alunos(alunos)
            
        elif opcao == "3":
            try:
                id_aluno = int(input("Digite o ID do aluno a atualizar: "))
                nome = input("Digite o novo nome: ")
                idade = int(input("Digite a nova idade: "))
                curso = input("Digite o novo curso: ")
                atualizar_aluno(cursor, conn, id_aluno, nome, idade, curso)
            except ValueError:
                print("ID e idade devem ser números inteiros!")
                
        elif opcao == "4":
            try:
                id_aluno = int(input("Digite o ID do aluno a deletar: "))
                deletar_aluno(cursor, conn, id_aluno)
            except ValueError:
                print("ID deve ser um número inteiro!")
                
        elif opcao == "5":
            campo = input("Consultar por (nome/curso): ").lower()
            if campo not in ["nome", "curso"]:
                print("Campo inválido! Use 'nome' ou 'curso'.")
                continue
            valor = input(f"Digite o valor a buscar em {campo}: ")
            alunos = consultar_alunos(cursor, campo, valor)
            exibir_alunos(alunos)
            
        elif opcao == "6":
            print("Saindo...")
            break
            
        else:
            print("Opção inválida! Tente novamente.")
    
    conn.close()

if __name__ == "__main__":
    main()