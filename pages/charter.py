import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Generador Charters | GM", page_icon="📄", layout="wide")

# CSS para ocultar el menú lateral y mantener estética limpia
st.markdown("""
    <style>
    [data-testid="collapsedControl"] { display: none; }
    </style>
""", unsafe_allow_html=True)

# Botón de regreso
if st.button("⬅️ Regresar al Portal de Inicio"):
    st.switch_page("app.py")

st.markdown("---")
st.title("📄 Generador de Project Charters (PMI)")
st.markdown("Captura los datos iniciales para generar el Acta de Constitución del Proyecto estructurada.")

# TABS
tab1, tab2, tab3, tab4 = st.tabs(["1. Info General", "2. Alcance", "3. Cronograma", "4. Riesgos y Presupuesto"])

with tab1:
    st.subheader("Información General")
    col1, col2 = st.columns(2)
    with col1:
        nombre_proyecto = st.text_input("Nombre del Proyecto", placeholder="Ej. Estrategia Nacional SDX")
        cliente = st.text_input("Cliente", placeholder="Ej. Sodexo, Emerson, Jumex...")
        sponsor = st.text_input("Patrocinador (Sponsor)", value="Besco IMP, S.A. de C.V.")
    with col2:
        gerente = st.text_input("Gerente de Proyecto", value="Gerardo Méndez Velázquez")
        fecha_inicio = st.date_input("Fecha de Inicio")
        fecha_fin = st.date_input("Fecha de Fin (Estimada)")

with tab2:
    st.subheader("Alcance y Entregables")
    objetivo = st.text_area("Objetivo del Proyecto (SMART)")
    entregables = st.text_area("Entregables Clave Obligatorios", 
                               placeholder="- Folios cargados en plataforma\n- Reportes fotográficos (MR_fecha_sucursal)\n- Matriz de alcance regional")
    fuera_alcance = st.text_area("Fuera de Alcance (Exclusiones de servicio)")

with tab3:
    st.subheader("Cronograma de Hitos Principales")
    colA, colB, colC = st.columns(3)
    with colA:
        hito1 = st.text_input("Hito 1", placeholder="Alta de usuarios")
        fecha_h1 = st.date_input("Fecha Hito 1", key="f1")
    with colB:
        hito2 = st.text_input("Hito 2", placeholder="Despliegue operativo")
        fecha_h2 = st.date_input("Fecha Hito 2", key="f2")
    with colC:
        hito3 = st.text_input("Hito 3", placeholder="Cierre y firma")
        fecha_h3 = st.date_input("Fecha Hito 3", key="f3")

with tab4:
    st.subheader("Riesgos y Estructura Operativa")
    riesgos = st.text_area("Riesgos Principales", 
                           placeholder="Ej. Pérdida de contrato por incumplimiento de SLAs.")
    col_pres1, col_pres2 = st.columns(2)
    with col_pres1:
        presupuesto = st.number_input("Fondo de Anticipo (MXN)", min_value=0.0, step=1000.0, value=30000.0)
    with col_pres2:
        esquema = st.selectbox("Esquema de Ejecución", ["Mixto", "Interno", "Subcontratado"])

st.divider()

if st.button("🚀 Procesar Project Charter", type="primary", use_container_width=True):
    if not nombre_proyecto or not cliente:
        st.error("Por favor, llena al menos el Nombre del Proyecto y el Cliente para continuar.")
    else:
        data = {
            "Área PMI": ["General", "General", "General", "General", "General", "General", 
                        "Alcance", "Alcance", "Alcance", 
                        "Cronograma", "Cronograma", "Cronograma",
                        "Riesgos y Costos", "Riesgos y Costos", "Riesgos y Costos"],
            "Concepto": ["Proyecto", "Cliente", "Sponsor", "Project Manager", "Fecha Inicio", "Fecha Fin",
                         "Objetivo", "Entregables", "Fuera de Alcance",
                         f"Hito 1: {hito1}", f"Hito 2: {hito2}", f"Hito 3: {hito3}",
                         "Riesgos", "Fondo Máximo Asignado", "Esquema de Ejecución"],
            "Definición": [nombre_proyecto, cliente, sponsor, gerente, fecha_inicio.strftime('%Y-%m-%d'), fecha_fin.strftime('%Y-%m-%d'),
                        objetivo, entregables, fuera_alcance,
                        fecha_h1.strftime('%Y-%m-%d'), fecha_h2.strftime('%Y-%m-%d'), fecha_h3.strftime('%Y-%m-%d'),
                        riesgos, f"${presupuesto:,.2f}", esquema]
        }
        
        df = pd.DataFrame(data)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Acta_PMI')
            worksheet = writer.sheets['Acta_PMI']
            worksheet.column_dimensions['A'].width = 20
            worksheet.column_dimensions['B'].width = 30
            worksheet.column_dimensions['C'].width = 80
        
        output.seek(0)
        
        st.success("¡Documento procesado exitosamente!")
        st.download_button(
            label="📥 Descargar Project Charter (.xlsx)",
            data=output,
            file_name=f"Charter_{nombre_proyecto.replace(' ', '_')}_{cliente.replace(' ', '_')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
            use_container_width=True
        )
