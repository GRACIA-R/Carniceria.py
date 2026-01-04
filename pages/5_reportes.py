import streamlit as st
import pandas as pd

from core.inventory import get_inventory, low_stock
from core.sales import sales_by_day, sales_by_product
from core.purchases import purchases_by_day
from core.cashflow import cash_summary
from core.kpis import kpis_globales

st.header("📊 Reportes y KPIs")

# ========================
# KPIs PRINCIPALES
# ========================
kpis = kpis_globales()

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Ventas totales", f"${kpis['ventas_totales']:.2f}")
col2.metric("🛒 Compras totales", f"${kpis['compras_totales']:.2f}")
col3.metric("📦 Stock total (kg)", f"{kpis['stock_total_kg']:.1f}")
col4.metric("📈 Margen bruto", f"${kpis['margen_bruto']:.2f}")

st.divider()

# ========================
# VENTAS
# ========================
st.subheader("📅 Ventas por día")
df_sales_day = sales_by_day()
st.line_chart(df_sales_day.set_index("fecha"))

st.subheader("🥩 Ventas por producto")
df_sales_prod = sales_by_product()
st.dataframe(df_sales_prod, use_container_width=True)

st.divider()

# ========================
# COMPRAS
# ========================
st.subheader("🚚 Compras por día")
df_purchases = purchases_by_day()
st.bar_chart(df_purchases.set_index("fecha"))

st.divider()

# ========================
# INVENTARIO
# ========================
st.subheader("📦 Inventario actual")
df_inventory = get_inventory()
st.dataframe(df_inventory, use_container_width=True)

st.subheader("⚠️ Productos con bajo stock")
df_low = low_stock()
st.dataframe(df_low, use_container_width=True)

from core.kpis import margen_por_producto

st.subheader("📈 Margen por producto")
df_margen = margen_por_producto()
st.dataframe(df_margen, use_container_width=True)
