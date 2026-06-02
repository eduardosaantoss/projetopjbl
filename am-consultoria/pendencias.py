from database import get_connection

def criar_pendencia(cliente_id, visita_id, descricao, prazo, prioridade, status='aberta'):
    """Cria uma nova pendência vinculada a um cliente e opcionalmente a uma visita."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pendencias (cliente_id, visita_id, descricao, prazo, prioridade, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (cliente_id, visita_id, descricao, prazo, prioridade, status))
    conn.commit()
    conn.close()

def listar_pendencias(cliente_id=None, apenas_abertas=False):
    """Lista pendências, opcionalmente filtradas por cliente ou status."""
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT p.*, c.nome as cliente_nome 
        FROM pendencias p 
        JOIN clientes c ON p.cliente_id = c.id
    """
    params = []
    
    conditions = []
    if cliente_id:
        conditions.append("p.cliente_id = ?")
        params.append(cliente_id)
    if apenas_abertas:
        conditions.append("p.status = 'aberta'")
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    # Ordenação por prioridade: Alta > Média > Baixa
    query += """ ORDER BY 
        CASE prioridade 
            WHEN 'Alta' THEN 1 
            WHEN 'Média' THEN 2 
            WHEN 'Baixa' THEN 3 
            ELSE 4 
        END, prazo ASC"""
        
    cursor.execute(query, params)
    pendencias = cursor.fetchall()
    conn.close()
    return pendencias

def atualizar_status_pendencia(pendencia_id, novo_status):
    """Atualiza o status de uma pendência."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE pendencias SET status = ? WHERE id = ?", (novo_status, pendencia_id))
    conn.commit()
    conn.close()

def excluir_pendencia(pendencia_id):
    """Exclui uma pendência específica."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pendencias WHERE id = ?", (pendencia_id,))
    conn.commit()
    conn.close()
