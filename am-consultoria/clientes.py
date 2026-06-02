
from database import get_connection


def cadastrar_cliente(nome, tipo, cidade, contato, telefone, email, obs):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clientes (nome, tipo_cliente, cidade, contato_principal, telefone, email, observacoes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (nome, tipo, cidade, contato, telefone, email, obs))
    conn.commit()
    cliente_id = cursor.lastrowid
    conn.close()
    return cliente_id


def listar_clientes(pesquisa=""):
    conn = get_connection()
    cursor = conn.cursor()
    if pesquisa:
        cursor.execute("SELECT * FROM clientes WHERE nome LIKE ? ORDER BY nome", (f"%{pesquisa}%",))
    else:
        cursor.execute("SELECT * FROM clientes ORDER BY nome")
    clientes = cursor.fetchall()
    conn.close()
    return clientes


def buscar_cliente_por_id(cliente_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
    cliente = cursor.fetchone()
    conn.close()
    return cliente


def adicionar_contato(cliente_id, nome, cargo, obs_comport, pref_comunic):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO contatos_cliente (cliente_id, nome, cargo, observacoes_comportamentais, preferencia_comunicacao)
        VALUES (?, ?, ?, ?, ?)
    """, (cliente_id, nome, cargo, obs_comport, pref_comunic))
    conn.commit()
    conn.close()


def listar_contatos(cliente_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contatos_cliente WHERE cliente_id = ?", (cliente_id,))
    contatos = cursor.fetchall()
    conn.close()
    return contatos


def excluir_cliente(cliente_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
    conn.commit()
    conn.close()

