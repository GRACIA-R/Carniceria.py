import pandas as pd
from core.db import get_connection


def kpis_globales():
    conn = get_connection()

    ventas = pd.read_sql(
        "SELECT COALESCE(SUM(total), 0) AS total FROM ventas",
        conn
    ).iloc[0, 0]

    compras = pd.read_sql(
        "SELECT COALESCE(SUM(costo_total), 0) AS total FROM compras",
        conn
    ).iloc[0, 0]

    stock_kg = pd.read_sql(
        "SELECT COALESCE(SUM(stock_kg), 0) AS total FROM productos",
        conn
    ).iloc[0, 0]

    valor_inventario = pd.read_sql(
        "SELECT COALESCE(SUM(stock_kg * costo_kg), 0) AS total FROM productos",
        conn
    ).iloc[0, 0]

    return {
        "ventas_totales": ventas,
        "compras_totales": compras,
        "stock_total_kg": stock_kg,
        "valor_inventario": valor_inventario,
        "margen_bruto": ventas - compras
    }


def margen_por_producto():
    conn = get_connection()

    return pd.read_sql(
        """
        SELECT
            nombre,
            costo_kg,
            precio_kg,
            stock_kg,
            (precio_kg - costo_kg) AS margen_kg,
            CASE
                WHEN precio_kg > 0
                THEN ROUND((precio_kg - costo_kg) / precio_kg * 100, 2)
                ELSE 0
            END AS margen_pct
        FROM productos
        ORDER BY margen_kg DESC
        """,
        conn
    )
