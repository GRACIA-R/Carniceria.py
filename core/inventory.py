import pandas as pd
from core.db import get_connection

def get_inventory():
    conn = get_connection()
    return pd.read_sql("SELECT * FROM productos", conn)

def low_stock(threshold=5):
    conn = get_connection()
    query = f"""
    SELECT nombre, stock_kg
    FROM productos
    WHERE stock_kg <= {threshold}
    """
    return pd.read_sql(query, conn)

