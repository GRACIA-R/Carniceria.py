import pandas as pd
from core.db import get_connection

def get_kpis():
    conn = get_connection()

    ventas = pd.read_sql(
        "SELECT COALESCE(SUM(total),0) as v FROM ventas", conn
    ).iloc[0]["v"]

    compras = pd.read_sql(
        "SELECT COALESCE(SUM(total),0) as c FROM compras", conn
    ).iloc[0]["c"]

    stock = pd.read_sql(
        """
        SELECT COALESCE(SUM(stock_kg),0) as stock
        FROM productos
        """,
        conn
    ).iloc[0]["stock"]

    margen = ventas - compras

    return {
        "ventas_totales": ventas,
        "compras_totales": compras,
        "stock_total_kg": stock,
        "margen_bruto": margen
    }



def margen_por_producto():
    conn = get_connection()

    return pd.read_sql(
        """
        SELECT
            nombre,
            costo,
            precio,
            stock,
            (precio - costo) AS margen_unitario,
            ROUND(
                CASE
                    WHEN precio > 0
                    THEN (precio - costo) / precio * 100
                    ELSE 0
                END, 2
            ) AS margen_pct
        FROM productos
        ORDER BY margen_unitario DESC
        """,
        conn
    )
