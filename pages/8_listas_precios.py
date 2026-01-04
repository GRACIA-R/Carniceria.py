import streamlit as st
import pandas as pd
from core.db import get_connection

st.title("💲 Listas de precios")

conn = get_connection()

# =========================
# LISTAS EXISTENTES
# =========================
st.subheader("📋 Listas de precios")

listas = pd.read_sql(
    "SELECT id, nombre, descripcion FROM listas_precios ORDER BY nombre",
    conn
)

st.dataframe(listas, use_container_width=True)

# =========================
# NUEVA LISTA
# =========================
st.subheader("➕ Crear nueva lista")

with st.form("nueva_lista", clear_on_submit=True):

    nombre_lista = st.text_input("Nombre de la lista *")
    descripcion = st.text_input("Descripción")

    submit = st.form_submit_button("Crear lista")

    if submit:

        if not nombre_lista.strip():
            st.error("El nombre es obligatorio")
            st.stop()

        conn.execute(
            """
            INSERT INTO listas_precios (nombre, descripcion)
            VALUES (?, ?)
            """,
            (nombre_lista.strip(), descripcion.strip())
        )

        conn.commit()
        st.success("✅ Lista creada correctamente")
        st.rerun()

# =========================
# ASIGNACIÓN DE PRECIOS
# =========================
st.divider()
st.subheader("🧮 Precios por producto")

listas = pd.read_sql("SELECT id, nombre FROM listas_precios", conn)
productos = pd.read_sql(
    "SELECT id, nombre, precio, unidad FROM productos ORDER BY nombre",
    conn
)

if listas.empty or productos.empty:
    st.warning("⚠️ Debes tener productos y listas de precios registradas.")
    st.stop()

lista_nombre = st.selectbox(
    "Selecciona lista",
    listas["nombre"].tolist()
)

lista_id = int(listas.loc[listas["nombre"] == lista_nombre].iloc[0]["id"])

st.markdown(f"### 📦 Productos – Lista **{lista_nombre}**")

for _, prod in productos.iterrows():

    precio_especial_df = pd.read_sql(
        """
        SELECT precio
        FROM precios_producto
        WHERE producto_id = ? AND lista_id = ?
        """,
        conn,
        params=(prod["id"], lista_id)
    )

    if not precio_especial_df.empty:
        precio_actual = precio_especial_df.iloc[0]["precio"]
        usa_base = False
    else:
        precio_actual = prod["precio"]
        usa_base = True

    col1, col2, col3 = st.columns([4, 2, 2])

    with col1:
        st.write(f"**{prod['nombre']}** ({prod['unidad']})")

    with col2:
        nuevo_precio = st.number_input(
            "Precio",
            min_value=0.0,
            value=float(precio_actual),
            step=0.5,
            key=f"precio_{lista_id}_{prod['id']}"
        )

    with col3:
        if st.button("Guardar", key=f"save_{lista_id}_{prod['id']}"):

            if usa_base and nuevo_precio == prod["precio"]:
                st.info("Usando precio base")
                continue

            conn.execute(
                """
                INSERT INTO precios_producto (producto_id, lista_id, precio)
                VALUES (?, ?, ?)
                ON CONFLICT(producto_id, lista_id)
                DO UPDATE SET precio = excluded.precio
                """,
                (prod["id"], lista_id, nuevo_precio)
            )

            conn.commit()
            st.success(f"Precio actualizado: {prod['nombre']}")
            st.rerun()
