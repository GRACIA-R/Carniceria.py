import streamlit as st
import pandas as pd
from core.db import get_connection

st.header("📦 Inventario")

conn = get_connection()
df = pd.read_sql("SELECT * FROM productos", conn)

st.dataframe(df, use_container_width=True)

with st.form("nuevo_producto"):
    nombre = st.text_input("Producto")
    costo = st.number_input("Costo ($/kg)")
    precio = st.number_input("Precio ($/kg)")
    stock = st.number_input("Stock inicial (kg)")
    submit = st.form_submit_button("Agregar")

    if submit:
        conn.execute(
            "INSERT INTO productos (nombre, costo_kg, precio_kg, stock_kg) VALUES (?, ?, ?, ?)",
            (nombre, costo, precio, stock)
        )
        conn.commit()
        st.success("Producto agregado")
