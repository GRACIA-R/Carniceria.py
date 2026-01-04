import streamlit as st
import pandas as pd
from core.db import get_connection
from datetime import date

st.header("🧾 Caja")

conn = get_connection()
df = pd.read_sql("SELECT * FROM caja ORDER BY fecha DESC", conn)

st.subheader("Movimientos")
st.dataframe(df, use_container_width=True)

st.subheader("Nuevo movimiento manual")

fecha = st.date_input("Fecha", date.today())
tipo = st.selectbox("Tipo", ["ingreso", "egreso"])
monto = st.number_input("Monto ($)", min_value=0.0)
descripcion = st.text_input("Descripción")

if st.button("Registrar movimiento"):
    conn.execute(
        "INSERT INTO caja (fecha, tipo, monto, descripcion) VALUES (?, ?, ?, ?)",
        (str(fecha), tipo, monto, descripcion)
    )
    conn.commit()
    st.success("Movimiento registrado")

