import streamlit as st
import pandas as pd
from core.db import get_connection
from datetime import date

st.header("💰 Ventas")

conn = get_connection()
productos = pd.read_sql("SELECT * FROM productos", conn)

producto = st.selectbox("Producto", productos["nombre"])
kg = st.number_input("Kg vendidos", min_value=0.0)
fecha = st.date_input("Fecha", date.today())

if st.button("Registrar venta"):
    p = productos[productos["nombre"] == producto].iloc[0]
    total = kg * p["precio_kg"]

    conn.execute(
        "INSERT INTO ventas (fecha, producto_id, kg, total) VALUES (?, ?, ?, ?)",
        (str(fecha), p["id"], kg, total)
    )

    conn.execute(
        "UPDATE productos SET stock_kg = stock_kg - ? WHERE id = ?",
        (kg, p["id"])
    )

    conn.commit()
    st.success(f"Venta registrada: ${total:.2f}")

