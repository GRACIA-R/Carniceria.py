import streamlit as st
import pandas as pd
from core.db import get_connection

st.title("📦 Inventario")

conn = get_connection()

# =========================
# ALTA DE PRODUCTO
# =========================
st.subheader("➕ Agregar producto")

with st.form("nuevo_producto", clear_on_submit=True):

    nombre = st.text_input("Nombre *")
    categoria = st.text_input("Categoría")
    unidad = st.selectbox("Unidad", ["kg", "pieza"])

    costo = st.number_input("Costo", min_value=0.0, step=0.5)
    precio = st.number_input("Precio base", min_value=0.0, step=0.5)
    stock = st.number_input("Stock inicial", min_value=0.0, step=0.1)

    submit = st.form_submit_button("Agregar")

    if submit:

        if not nombre.strip():
            st.error("El nombre es obligatorio")
            st.stop()

        conn.execute(
            """
            INSERT INTO productos
            (nombre, categoria, costo, precio, stock, unidad)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                nombre.strip(),
                categoria.strip(),
                costo,
                precio,
                stock,
                unidad
            )
        )

        conn.commit()
        st.success("✅ Producto agregado correctamente")
        st.rerun()

# =========================
# INVENTARIO ACTUAL
# =========================
st.divider()
st.subheader("📋 Inventario actual")

productos = pd.read_sql(
    """
    SELECT
        id,
        nombre,
        categoria,
        stock,
        unidad,
        costo,
        precio
    FROM productos
    ORDER BY nombre
    """,
    conn
)

st.dataframe(productos, width="stretch")
