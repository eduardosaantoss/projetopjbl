
from database import get_connection
from datetime import datetime


def registrar_visita(cliente_id, data_visita, tipo, resumo, contexto_humano, responsavel, prioridade):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO visitas (cliente_id, data_visita, tipo_visita, resumo, contexto_humano, responsavel, prioridade)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (cliente_id, data_visita, tipo, resumo, contexto_humano, responsavel, prioridade))
    conn.commit()
    visita_id = cursor.lastrowid
    conn.close()
    return visita_id


def listar_visitas(cliente_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    if cliente_id:
        cursor.execute("""
            SELECT v.*, c.nome as cliente_nome 
            FROM visitas v 
            JOIN clientes c ON v.cliente_id = c.id 
            WHERE v.cliente_id = ? 
            ORDER BY data_visita DESC
        """, (cliente_id,))
    else:
        cursor.execute("""
            SELECT v.*, c.nome as cliente_nome 
            FROM visitas v 
            JOIN clientes c ON v.cliente_id = c.id 
            ORDER BY data_visita DESC
        """)
    visitas = cursor.fetchall()
    conn.close()
    return visitas


def excluir_visita(visita_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM visitas WHERE id = ?", (visita_id,))
    conn.commit()
    conn.close()

