import streamlit as st

# 1. Configuración de la página (DEBE SER LA PRIMERA LÍNEA DE STREAMLIT)
st.set_page_config(
    page_title="Portal de Operaciones | Besco", 
    page_icon="🏢", 
    layout="wide"
)

# --- FUNCIONES DE CADA APLICACIÓN ---

def pagina_inicio():
    """Renderiza el portal de inicio principal"""
    st.title("🏢 Portal Central de Operaciones y Mantenimiento")
    st.markdown("---")
    st.markdown("Bienvenido al ecosistema central de herramientas. Selecciona una aplicación en el menú lateral para comenzar a operar.")
    
    # Grid de visualización de las apps disponibles
    st.subheader("Herramientas Disponibles")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("#### 📄 Generador de Charters\n\nCrea Actas de Constitución PMI (Formato Excel) estandarizadas para arranques de implementaciones (Ej. mpservice, Sodexo).")
    
    with col2:
        st.warning("#### ⚙️ Control de Asistencia\n\n*(Próximamente)* Herramienta para gestión y geolocalización de técnicos en sitio.")
        
    with col3:
        st.success("#### 📝 Cotizaciones\n\n*(Próximamente)* Motor de propuestas con reglas de utilidad por partida y reportes fotográficos.")

def app_project_charter():
    """Renderiza la aplicación del Generador de Charters"""
    st.title("📄 Generador de Project Charters (PMI)")
    st.info("Aquí incrustaremos el código completo del formulario y la generación del Excel en el siguiente paso.")

# --- SISTEMA DE NAVEGACIÓN (SIDEBAR) ---

def main():
    st.sidebar.title("Navegación del Portal")
    st.sidebar.markdown("---")

    # Definir las opciones del menú
    opciones_menu = [
        "🏠 Inicio", 
        "📄 Generador de Charters"
    ]
    
    # Selector de navegación
    eleccion = st.sidebar.radio("Selecciona un módulo:", opciones_menu)

    st.sidebar.markdown("---")
    st.sidebar.caption("Operaciones y Mantenimiento | Besco IMP, S.A. de C.V.")

    # Lógica de ruteo de las páginas
    if eleccion == "🏠 Inicio":
        pagina_inicio()
    elif eleccion == "📄 Generador de Charters":
        app_project_charter()

# Ejecución principal de la app
if __name__ == "__main__":
    main()
