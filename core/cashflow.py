import pandas as pd
from core.db import get_connection

def cash_summary():
    conn = get_connection()
    return pd.read_sql("""
        SELECT
            fecha,
            SUM(CASE WHEN tipo='ingreso' THEN monto ELSE 0 END) as ingresos,
            SUM(CASE WHEN tipo='egreso' THEN monto ELSE 0 END) as egresos
        FROM caja
        GROUP BY fecha
        ORDER BY fecha
    """, conn)

