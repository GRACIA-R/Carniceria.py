import streamlit as st
from core.db import init_db

init_db()

# =========================
# CONFIGURACIÓN GENERAL
# =========================
st.set_page_config(
    page_title="Carnicería TORO 2000",
    page_icon="🥩",
    layout="wide"
)

# =========================
# HEADER
# =========================
st.title("🥩 Carnicería TORO 2000")
st.markdown("""
**Sistema de inventarios, ventas, compras y control financiero**  
""")

st.divider()

# =========================
# ESTADO GLOBAL (FUTURO)
# =========================
if "usuario" not in st.session_state:
    st.session_state.usuario = "admin"

# =========================
# PANEL PRINCIPAL
# =========================
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📌 ¿Qué puedes hacer aquí?")
    st.markdown("""
    - 📦 Controlar inventarios en tiempo real  
    - 💰 Registrar ventas  
    - 🚚 Registrar compras  
    - 🧾 Controlar caja  
    - 📊 Analizar reportes y márgenes  
    """)

with col2:
    st.subheader("⚙️ Estado del sistema")
    st.success("Aplicación activa")
    st.info("Modo: Local / Streamlit Cloud")
    st.write("Usuario:", st.session_state.usuario)

st.divider()

# =========================
# INSTRUCCIONES OPERATIVAS
# =========================
st.subheader("🧠 Flujo recomendado diario")

st.markdown("""
1️⃣ Registrar **compras** al recibir canal  
2️⃣ Registrar **ventas** durante el día  
3️⃣ Revisar **inventario**  
4️⃣ Registrar **egresos** (luz, agua, etc.)  
5️⃣ Revisar **reportes y márgenes**
""")

st.divider()

# =========================
# FOOTER
# =========================
st.caption("""
Carnicería Digital Twin  
Desarrollado en Python + Streamlit  
Enfoque: control, optimización y escalabilidad
""")
