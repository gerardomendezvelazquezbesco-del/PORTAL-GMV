import streamlit as st

st.set_page_config(page_title="Nueva App | GM", page_icon="🚧", layout="wide")

st.markdown("""<style>[data-testid="collapsedControl"] { display: none; }</style>""", unsafe_allow_html=True)

if st.button("⬅️ Regresar al Portal de Inicio"):
    st.switch_page("app.py")

st.markdown("---")
st.title("🚧 Nuevo Módulo en Desarrollo")
st.warning("Espacio reservado. Listo para recibir código nuevo.")
