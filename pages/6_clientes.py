import streamlit as st
import pandas as pd
from core.db import get_connection

st.title("👥 Clientes")

conn = get_connection()

# Alta de cliente
with st.form("nuevo_cliente"):
    nombre = st.text_input("Nombre")
    telefono = st.text_input("Teléfono")
    email = st.text_input("Email")

    listas = pd.read_sql("SELECT id, nombre FROM listas_precios", conn)
    lista = st.selectbox(
        "Lista de precios",
        listas["nombre"]
    )

    submit = st.form_submit_button("Guardar")

    if submit:
        lista_id = listas[listas["nombre"] == lista]["id"].values[0]
        conn.execute(
            """INSERT INTO clientes (nombre, telefono, email, lista_precio_id)
               VALUES (?, ?, ?, ?)""",
            (nombre, telefono, email, lista_id)
        )
        conn.commit()
        st.success("Cliente registrado")
