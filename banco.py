import sqlite3
from cliente import Cliente


class GerenciadorClientes:
    def __init__(self, caminho_banco="techbairro.db"):
        self.caminho_banco = caminho_banco
        self.criar_tabela()

    def conectar(self):
        return sqlite3.connect(self.caminho_banco)

    def criar_tabela(self):
        with self.conectar() as conexao:
            conexao.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    telefone TEXT,
                    email TEXT,
                    endereco TEXT
                )
            """)

    def adicionar(self, cliente):
        with self.conectar() as conexao:
            cursor = conexao.execute(
                """INSERT INTO clientes (nome, telefone, email, endereco)
                   VALUES (?, ?, ?, ?)""",
                (cliente.nome, cliente.telefone, cliente.email, cliente.endereco)
            )
            cliente.id = cursor.lastrowid

    def listar(self):
        with self.conectar() as conexao:
            linhas = conexao.execute(
                """SELECT id, nome, telefone, email, endereco
                   FROM clientes ORDER BY nome"""
            ).fetchall()

        return [
            Cliente(nome, telefone, email, endereco, id_cliente)
            for (id_cliente, nome, telefone, email, endereco) in linhas
        ]

    def atualizar(self, id_cliente, novo_cliente):
        with self.conectar() as conexao:
            cursor = conexao.execute(
                """UPDATE clientes
                   SET nome = ?, telefone = ?, email = ?, endereco = ?
                   WHERE id = ?""",
                (novo_cliente.nome, novo_cliente.telefone, novo_cliente.email,
                 novo_cliente.endereco, id_cliente)
            )
        return cursor.rowcount == 1

    def remover(self, id_cliente):
        with self.conectar() as conexao:
            cursor = conexao.execute(
                "DELETE FROM clientes WHERE id = ?", (id_cliente,)
            )
        return cursor.rowcount == 1

    def total(self):
        with self.conectar() as conexao:
            return conexao.execute(
                "SELECT COUNT(*) FROM clientes"
            ).fetchone()[0]
