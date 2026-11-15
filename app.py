import streamlit as st

# 1. Configuración de la página
st.set_page_config(
    page_title="Soluciones Integrales | GM", 
    page_icon="🚀", 
    layout="wide"
)

# 2. CSS para Botones Gigantes y Ocultar Menú Lateral
st.markdown("""
    <style>
    button[kind="primary"] {
        background-color: #0056b3 !important;
        color: white !important;
        font-size: 24px !important;
        font-weight: bold !important;
        padding: 30px 24px !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 10px #003d82 !important;
        transition: all 0.1s ease !important;
        width: 100% !important;
    }
    button[kind="primary"]:active { box-shadow: 0 4px #003d82 !important; transform: translateY(6px) !important; }
    button[kind="primary"]:hover { background-color: #0069d9 !important; color: white !important; }
    [data-testid="collapsedControl"] { display: none; }
    </style>
""", unsafe_allow_html=True)

# 3. Interfaz del Portal
st.title("🚀 Portal de Soluciones Integrales | Gerardo Méndez")
st.markdown("Plataforma central de herramientas personalizadas para la optimización de operaciones, mantenimiento y gestión de facilities.")
st.markdown("---")

st.write("")
st.write("")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📄 Generador Charters", type="primary", use_container_width=True):
        st.switch_page("pages/charter.py")
    st.info("Crea Actas de Constitución PMI (Formato Excel) estandarizadas para arranques de proyectos.")

with col2:
    if st.button("🚧 Próxima App", type="primary", use_container_width=True):
        st.switch_page("pages/proxima.py")
    st.warning("*(En desarrollo)* Espacio reservado para la próxima herramienta de tu portafolio.")
    
with col3:
    if st.button("❄️ Carga Térmica", type="primary", use_container_width=True):
        st.switch_page("pages/carga.py")
    st.success("*(Próximamente)* Calculadora de requerimientos y capacidad HVAC para proyectos.")
