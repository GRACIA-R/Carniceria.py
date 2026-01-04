import streamlit as st
import pandas as pd
from core.db import get_connection

st.title("👥 Clientes")

conn = get_connection()

# =========================
# CARGA DE LISTAS DE PRECIOS
# =========================
listas = pd.read_sql(
    "SELECT id, nombre FROM listas_precios",
    conn
)

if listas.empty:
    st.warning("⚠️ No existen listas de precios. Crea al menos una antes de registrar clientes.")
    st.stop()

# =========================
# ALTA DE CLIENTE
# =========================
st.subheader("➕ Nuevo cliente")

with st.form("nuevo_cliente", clear_on_submit=True):

    nombre = st.text_input("Nombre *")
    telefono = st.text_input("Teléfono")
    email = st.text_input("Email")

    lista_nombre = st.selectbox(
        "Lista de precios",
        listas["nombre"].tolist()
    )

    submit = st.form_submit_button("Guardar")

    if submit:

        if not nombre.strip():
            st.error("El nombre del cliente es obligatorio")
            st.stop()

        lista_row = listas.loc[listas["nombre"] == lista_nombre]

        if lista_row.empty:
            st.error("Lista de precios inválida")
            st.stop()

        lista_id = int(lista_row.iloc[0]["id"])

        conn.execute(
            """
            INSERT INTO clientes (nombre, telefono, email, lista_precio_id)
            VALUES (?, ?, ?, ?)
            """,
            (nombre.strip(), telefono.strip(), email.strip(), lista_id)
        )

        conn.commit()

        st.success("✅ Cliente registrado correctamente")

# =========================
# LISTADO DE CLIENTES
# =========================
st.divider()
st.subheader("📋 Clientes registrados")

clientes = pd.read_sql(
    """
    SELECT c.id, c.nombre, c.telefono, c.email, lp.nombre AS lista
    FROM clientes c
    LEFT JOIN listas_precios lp ON c.lista_precio_id = lp.id
    WHERE c.activo = 1
    ORDER BY c.nombre
    """,
    conn
)

st.dataframe(clientes, use_container_width=True)
