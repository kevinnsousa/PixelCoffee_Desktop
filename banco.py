import sqlite3

class BancoDados:
    def __init__(self, db_name="pixelcoffee.db"):
        self.db_name = db_name
        self.criar_tabelas()

    def conectar(self):
        return sqlite3.connect(self.db_name)

    def criar_tabelas(self):
        with self.conectar() as conn:
            cursor = conn.cursor()
            
            # Tabela de Produtos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    preco REAL NOT NULL
                )
            ''')
            
            # Tabela de Clientes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL
                )
            ''')
            
            # Tabela de Pedidos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pedidos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_nome TEXT NOT NULL,
                    itens TEXT NOT NULL,
                    total REAL NOT NULL
                )
            ''')
            conn.commit()
            
        # Inserir dados padrão se o banco estiver limpo
        self.popular_dados_iniciais()

    def popular_dados_iniciais(self):
        with self.conectar() as conn:
            cursor = conn.cursor()
            
            # Verifica se a tabela produtos está vazia
            cursor.execute("SELECT COUNT(*) FROM produtos")
            if cursor.fetchone()[0] == 0:
                produtos_iniciais = [
                    ("Espresso Tradicional", 6.50),
                    ("Cappuccino Italiano", 12.00),
                    ("Pão de Queijo", 5.00),
                    ("Bolo de Chocolate", 8.00)
                ]
                cursor.executemany("INSERT INTO produtos (nome, preco) VALUES (?, ?)", produtos_iniciais)
            
            # Verifica se a tabela clientes está vazia
            cursor.execute("SELECT COUNT(*) FROM clientes")
            if cursor.fetchone()[0] == 0:
                clientes_iniciais = [
                    ("João",),
                    ("Arthur",),
                    ("Amanda",),
                    ("Liz",)
                ]
                cursor.executemany("INSERT INTO clientes (nome) VALUES (?)", clientes_iniciais)

            conn.commit()

    def inserir_produto(self, nome, preco):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO produtos (nome, preco) VALUES (?, ?)", (nome, preco))
            conn.commit()

    def listar_produtos(self):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, preco FROM produtos")
            return cursor.fetchall()

    def inserir_cliente(self, nome):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO clientes (nome) VALUES (?)", (nome,))
            conn.commit()

    def listar_clientes(self):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome FROM clientes")
            return cursor.fetchall()

    def inserir_pedido(self, cliente_nome, itens, total):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO pedidos (cliente_nome, itens, total) VALUES (?, ?, ?)",
                (cliente_nome, itens, total)
            )
            conn.commit()

    def listar_pedidos(self):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, cliente_nome, itens, total FROM pedidos")
            return cursor.fetchall()