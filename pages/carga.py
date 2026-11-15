import streamlit as st

st.set_page_config(page_title="Carga Térmica | GM", page_icon="❄️", layout="wide")

st.markdown("""<style>[data-testid="collapsedControl"] { display: none; }</style>""", unsafe_allow_html=True)

if st.button("⬅️ Regresar al Portal de Inicio"):
    st.switch_page("app.py")

st.markdown("---")
st.title("❄️ Calculadora de Carga Térmica y Capacidad HVAC")
st.info("Módulo en construcción. Aquí integraremos la lógica de cálculos térmicos.")
