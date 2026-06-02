from database import get_connection

def cadastrar_contrato(cliente_id, tipo, valor, data_inicio, data_fim, obs):
    """Cadastra um novo contrato para um cliente."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO contratos (cliente_id, tipo_contrato, valor, data_inicio, data_fim, observacoes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (cliente_id, tipo, valor, data_inicio, data_fim, obs))
    conn.commit()
    conn.close()

def listar_contratos(cliente_id=None):
    """Lista todos os contratos ou filtra por cliente."""
    conn = get_connection()
    cursor = conn.cursor()
    if cliente_id:
        cursor.execute("""
            SELECT con.*, cli.nome as cliente_nome 
            FROM contratos con
            JOIN clientes cli ON con.cliente_id = cli.id
            WHERE con.cliente_id = ?
            ORDER BY data_fim DESC
        """, (cliente_id,))
    else:
        cursor.execute("""
            SELECT con.*, cli.nome as cliente_nome 
            FROM contratos con
            JOIN clientes cli ON con.cliente_id = cli.id
            ORDER BY data_fim DESC
        """)
    contratos = cursor.fetchall()
    conn.close()
    return contratos

def excluir_contrato(contrato_id):
    """Exclui um contrato específico."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contratos WHERE id = ?", (contrato_id,))
    conn.commit()
    conn.close()

def calcular_valor_total_contratos():
    """Calcula o valor total de todos os contratos ativos."""
    conn = get_connection()
    cursor = conn.cursor()
    # Consideramos apenas contratos que ainda não venceram ou todos? 
    # Vou considerar todos por enquanto, ou podemos filtrar por data.
    cursor.execute("SELECT SUM(valor) FROM contratos")
    total = cursor.fetchone()[0]
    conn.close()
    return total if total else 0.0
