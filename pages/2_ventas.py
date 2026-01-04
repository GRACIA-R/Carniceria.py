import streamlit as st
import pandas as pd
from core.db import get_connection
from datetime import date

st.header("💰 Ventas")

conn = get_connection()

# =========================
# CARGA DE DATOS BASE
# =========================
clientes = pd.read_sql(
    "SELECT id, nombre, lista_precio_id FROM clientes WHERE activo = 1",
    conn
)

productos = pd.read_sql(
    "SELECT id, nombre, precio, stock, unidad FROM productos",
    conn
)

# =========================
# SELECCIÓN DE CLIENTE
# =========================
st.subheader("👤 Cliente")

cliente_nombre = st.selectbox(
    "Selecciona cliente",
    clientes["nombre"]
)

cliente = clientes[clientes["nombre"] == cliente_nombre].iloc[0]
cliente_id = cliente["id"]
lista_precio_id = cliente["lista_precio_id"]

# =========================
# SELECCIÓN DE PRODUCTO
# =========================
st.subheader("🥩 Producto")

producto_nombre = st.selectbox(
    "Producto",
    productos["nombre"]
)

producto = productos[productos["nombre"] == producto_nombre].iloc[0]

st.caption(
    f"Stock disponible: {producto['stock']} {producto['unidad']}"
)

# =========================
# PRECIO SEGÚN LISTA
# =========================
precio_venta = producto["precio"]

if pd.notna(lista_precio_id):
    precio_df = pd.read_sql(
        """
        SELECT precio
        FROM precios_producto
        WHERE producto_id = ? AND lista_id = ?
        """,
        conn,
        params=(producto["id"], int(lista_precio_id))
    )

    if not precio_df.empty:
        precio_venta = precio_df.iloc[0]["precio"]
        st.info(f"💲 Precio especial aplicado: ${precio_venta:.2f}")
    else:
        st.info(f"💲 Precio público: ${precio_venta:.2f}")
else:
    st.info(f"💲 Precio público: ${precio_venta:.2f}")

# =========================
# DATOS DE VENTA
# =========================
cantidad = st.number_input(
    f"Cantidad ({producto['unidad']})",
    min_value=0.0,
    step=0.1
)

fecha = st.date_input("Fecha", date.today())

total = cantidad * precio_venta

st.metric("💵 Total", f"${total:,.2f}")

# =========================
# REGISTRO DE VENTA
# =========================
if st.button("Registrar venta", type="primary"):

    if cantidad <= 0:
        st.error("La cantidad debe ser mayor a cero")
        st.stop()

    if cantidad > producto["stock"]:
        st.error("Stock insuficiente")
        st.stop()

    cursor = conn.cursor()

    # --- Inserta venta (cabecera) ---
    cursor.execute(
        """
        INSERT INTO ventas (fecha, cliente_id, total)
        VALUES (?, ?, ?)
        """,
        (str(fecha), cliente_id, total)
    )

    venta_id = cursor.lastrowid

    # --- Detalle de venta ---
    cursor.execute(
        """
        INSERT INTO venta_detalle
        (venta_id, producto_id, cantidad, precio)
        VALUES (?, ?, ?, ?)
        """,
        (venta_id, producto["id"], cantidad, precio_venta)
    )

    # --- Actualiza stock ---
    cursor.execute(
        """
        UPDATE productos
        SET stock = stock - ?
        WHERE id = ?
        """,
        (cantidad, producto["id"])
    )

    # --- Registra en caja ---
    cursor.execute(
        """
        INSERT INTO caja (fecha, tipo, concepto, monto)
        VALUES (?, 'ingreso', ?, ?)
        """,
        (str(fecha), f"Venta a {cliente_nombre}", total)
    )

    conn.commit()

    st.success(f"✅ Venta registrada correctamente por ${total:,.2f}")
    st.rerun()
