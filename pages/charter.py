import streamlit as st
import pandas as pd
import io
import json
import google.generativeai as genai

st.set_page_config(page_title="Generador Charters | GM", page_icon="📄", layout="wide")

# Ocultar menú lateral
st.markdown("""<style>[data-testid="collapsedControl"] { display: none; }</style>""", unsafe_allow_html=True)

# Configuración de Gemini AI usando los secretos de Streamlit
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    modelo_ia = genai.GenerativeModel('gemini-1.5-flash')
    ia_disponible = True
except Exception:
    ia_disponible = False

if st.button("⬅️ Regresar al Portal de Inicio"):
    st.switch_page("app.py")

st.markdown("---")
st.title("📄 Generador de Project Charters (IA PMI)")
st.markdown("Captura ideas clave. El asistente de IA expandirá la información a estándar PMI enfocado en Facility Management y Operaciones.")

if not ia_disponible:
    st.warning("⚠️ La API Key de Gemini no está configurada en los Secrets de Streamlit. La app funcionará en modo manual.")

tab1, tab2, tab3, tab4 = st.tabs(["1. Info General", "2. Alcance (Borrador)", "3. Cronograma", "4. Riesgos y Presupuesto"])

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
    st.subheader("Alcance y Entregables (Ideas Base)")
    st.info("💡 Escribe solo ideas breves. La Inteligencia Artificial redactará los párrafos formales.")
    objetivo_base = st.text_area("Objetivo (Idea principal)", placeholder="Ej. Cumplir con el mantenimiento MP y MR a nivel nacional.")
    entregables_base = st.text_area("Entregables clave", placeholder="Ej. Reportes con fotos MR_fecha, plataforma Value Keap.")
    fuera_alcance = st.text_area("Fuera de Alcance (Exclusiones)", placeholder="Ej. Obra civil, reparaciones mayores no aprobadas.")

with tab3:
    st.subheader("Cronograma de Hitos Principales")
    colA, colB, colC = st.columns(3)
    with colA:
        hito1 = st.text_input("Hito 1", placeholder="Planeación y recursos")
        fecha_h1 = st.date_input("Fecha Hito 1", key="f1")
    with colB:
        hito2 = st.text_input("Hito 2", placeholder="Despliegue operativo")
        fecha_h2 = st.date_input("Fecha Hito 2", key="f2")
    with colC:
        hito3 = st.text_input("Hito 3", placeholder="Cierre y evaluación")
        fecha_h3 = st.date_input("Fecha Hito 3", key="f3")

with tab4:
    st.subheader("Riesgos y Estructura Operativa")
    riesgos_base = st.text_area("Riesgos (Ideas breves)", placeholder="Ej. Pérdida del contrato por SLA, falta de diésel.")
    col_pres1, col_pres2 = st.columns(2)
    with col_pres1:
        presupuesto = st.number_input("Fondo de Anticipo Máximo (MXN)", min_value=0.0, step=1000.0, value=30000.0)
    with col_pres2:
        esquema = st.selectbox("Esquema de Ejecución", ["Mixto", "Interno", "Subcontratado"])

st.divider()

if st.button("🚀 Procesar Project Charter con IA", type="primary", use_container_width=True):
    if not nombre_proyecto or not cliente:
        st.error("Por favor, llena al menos el Nombre del Proyecto y el Cliente.")
    else:
        objetivo_final = objetivo_base
        entregables_final = entregables_base
        riesgos_final = riesgos_base
        
        # Intervención de la IA
        if ia_disponible:
            with st.spinner("🧠 Analizando operación e inyectando estándar PMI..."):
                prompt = f"""
                Eres un Project Manager certificado (PMP). Tu usuario es Gerardo Méndez de Besco IMP, S.A. de C.V., empresa especializada en facility management, mantenimiento HVAC y servicios generales.
                Expande las siguientes notas breves en redacción formal y corporativa bajo el estándar PMI.
                
                Proyecto: {nombre_proyecto}
                Cliente: {cliente}
                Objetivo base: {objetivo_base}
                Entregables base: {entregables_base}
                Riesgos base: {riesgos_base}
                
                Devuelve ÚNICAMENTE un objeto JSON válido con estas 3 claves, sin formato markdown extra, solo el JSON puro:
                {{
                    "objetivo": "Redacta un objetivo SMART detallado.",
                    "entregables": "Lista detallada en un solo párrafo o separada por guiones simples.",
                    "riesgos": "Describe los riesgos formales y agrega un plan de respuesta/mitigación breve para cada uno."
                }}
                """
                try:
                    respuesta = modelo_ia.generate_content(prompt)
                    # Limpieza del texto devuelto para asegurar que el JSON se lea correctamente
                    texto_limpio = respuesta.text.replace("```json", "").replace("```", "").strip()
                    datos_ia = json.loads(texto_limpio)
                    
                    objetivo_final = datos_ia.get("objetivo", objetivo_base)
                    entregables_final = datos_ia.get("entregables", entregables_base)
                    riesgos_final = datos_ia.get("riesgos", riesgos_base)
                    st.success("✨ ¡Texto expandido con éxito mediante IA!")
                except Exception as e:
                    st.warning(f"No se pudo conectar con la IA para la expansión. Se usará el texto original. (Error: {e})")
        
        # Generación del DataFrame
        data = {
            "Área PMI": ["General", "General", "General", "General", "General", "General", 
                        "Alcance", "Alcance", "Alcance", 
                        "Cronograma", "Cronograma", "Cronograma",
                        "Riesgos y Costos", "Riesgos y Costos", "Riesgos y Costos"],
            "Concepto": ["Proyecto", "Cliente", "Sponsor", "Project Manager", "Fecha Inicio", "Fecha Fin",
                         "Objetivo (SMART)", "Entregables", "Fuera de Alcance",
                         f"Hito 1: {hito1}", f"Hito 2: {hito2}", f"Hito 3: {hito3}",
                         "Riesgos y Mitigación", "Fondo Máximo Asignado", "Esquema de Ejecución"],
            "Definición": [nombre_proyecto, cliente, sponsor, gerente, fecha_inicio.strftime('%Y-%m-%d'), fecha_fin.strftime('%Y-%m-%d'),
                        objetivo_final, entregables_final, fuera_alcance,
                        fecha_h1.strftime('%Y-%m-%d'), fecha_h2.strftime('%Y-%m-%d'), fecha_h3.strftime('%Y-%m-%d'),
                        riesgos_final, f"${presupuesto:,.2f}", esquema]
        }
        
        df = pd.DataFrame(data)
        
        # Visualización previa para que veas el trabajo de la IA
        st.markdown("### 📋 Vista Previa del Documento Mejorado")
        st.dataframe(df, use_container_width=True)
        
        # Creación del Excel en memoria
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Acta_PMI')
            worksheet = writer.sheets['Acta_PMI']
            worksheet.column_dimensions['A'].width = 20
            worksheet.column_dimensions['B'].width = 30
            worksheet.column_dimensions['C'].width = 100 # Más ancho para el texto de la IA
        
        output.seek(0)
        
        st.download_button(
            label="📥 Descargar Project Charter Aprobado (.xlsx)",
            data=output,
            file_name=f"Charter_PMI_{nombre_proyecto.replace(' ', '_')}_{cliente.replace(' ', '_')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
            use_container_width=True
        )
