import pandas as pd
from core.db import get_connection

def sales_by_day():
    conn = get_connection()
    return pd.read_sql("""
        SELECT fecha, SUM(total) as ventas
        FROM ventas
        GROUP BY fecha
        ORDER BY fecha
    """, conn)


def sales_by_product():
    conn = get_connection()

    return pd.read_sql(
        """
        SELECT 
            p.nombre,
            SUM(v.cantidad) AS kg_vendidos,
            SUM(v.total) AS total
        FROM ventas v
        JOIN productos p ON v.producto_id = p.id
        GROUP BY p.nombre
        ORDER BY total DESC
        """,
        conn
    )


