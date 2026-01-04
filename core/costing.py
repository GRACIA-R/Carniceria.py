from core.db import get_connection

def actualizar_costo_promedio(producto_id, kg_compra, costo_total):
    conn = get_connection()

    prod = conn.execute(
        "SELECT stock_kg, costo_kg FROM productos WHERE id = ?",
        (producto_id,)
    ).fetchone()

    stock_actual, costo_actual = prod

    costo_compra_kg = costo_total / kg_compra if kg_compra > 0 else 0

    if stock_actual <= 0:
        nuevo_costo = costo_compra_kg
    else:
        nuevo_costo = (
            (stock_actual * costo_actual) +
            (kg_compra * costo_compra_kg)
        ) / (stock_actual + kg_compra)

    conn.execute(
        "UPDATE productos SET costo_kg = ? WHERE id = ?",
        (nuevo_costo, producto_id)
    )

    conn.commit()
