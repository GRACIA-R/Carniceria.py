import pandas as pd
from core.db import get_connection


def kpis_globales():
    conn = get_connection()

    ventas = pd.read_sql(
        "SELECT COALESCE(SUM(total), 0) AS total FROM ventas",
        conn
    ).iloc[0, 0]

    compras = pd.read_sql(
        """
        SELECT COALESCE(SUM(kg * costo), 0) AS total
        FROM compras
        """,
        conn
    ).iloc[0, 0]

    stock_total = pd.read_sql(
        "SELECT COALESCE(SUM(stock), 0) AS total FROM productos",
        conn
    ).iloc[0, 0]

    valor_inventario = pd.read_sql(
        """
        SELECT COALESCE(SUM(stock * costo), 0) AS total
        FROM productos
        """,
        conn
    ).iloc[0, 0]

    return {
        "ventas_totales": ventas,
        "compras_totales": compras,
        "stock_total": stock_total,
        "valor_inventario": valor_inventario,
        "margen_bruto": ventas - compras
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
