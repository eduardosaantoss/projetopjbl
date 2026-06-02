import sqlite3
import os

DB_NAME = "am_consultoria.db"

def get_connection():
    """Retorna uma conexão com o banco de dados SQLite."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def criar_tabelas():
    """Cria as tabelas do banco de dados se não existirem."""
    conn = get_connection()
    cursor = conn.cursor()

    # Tabela de Clientes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        tipo_cliente TEXT,
        cidade TEXT,
        contato_principal TEXT,
        telefone TEXT,
        email TEXT,
        observacoes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Tabela de Contatos do Cliente
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contatos_cliente (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        nome TEXT NOT NULL,
        cargo TEXT,
        observacoes_comportamentais TEXT,
        preferencia_comunicacao TEXT,
        FOREIGN KEY (cliente_id) REFERENCES clientes (id) ON DELETE CASCADE
    )
    """)

    # Tabela de Visitas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS visitas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        data_visita TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        tipo_visita TEXT,
        resumo TEXT,
        contexto_humano TEXT NOT NULL,
        responsavel TEXT,
        prioridade TEXT,
        FOREIGN KEY (cliente_id) REFERENCES clientes (id) ON DELETE CASCADE
    )
    """)

    # Tabela de Pendências
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pendencias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        visita_id INTEGER,
        descricao TEXT NOT NULL,
        prazo TEXT,
        status TEXT DEFAULT 'aberta',
        prioridade TEXT,
        FOREIGN KEY (cliente_id) REFERENCES clientes (id) ON DELETE CASCADE,
        FOREIGN KEY (visita_id) REFERENCES visitas (id) ON DELETE CASCADE
    )
    """)

    # Tabela de Contratos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contratos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        tipo_contrato TEXT,
        valor REAL,
        data_inicio TEXT,
        data_fim TEXT,
        observacoes TEXT,
        FOREIGN KEY (cliente_id) REFERENCES clientes (id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_tabelas()
    print("Banco de dados e tabelas criados com sucesso.")
