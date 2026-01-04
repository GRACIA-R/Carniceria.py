import pandas as pd
from core.db import get_connection

def purchases_by_day():
    conn = get_connection()
    return pd.read_sql("""
        SELECT fecha, SUM(costo_total) as compras
        FROM compras
        GROUP BY fecha
        ORDER BY fecha
    """, conn)

