import streamlit as st

st.set_page_config(
    page_title="Titulacion Miris",
    page_icon="✈️",
    layout="wide"
)

st.title("Proceso a titularme")
st.subheader("Formación, legislación y progreso académico")

st.markdown("---")

st.write("Bienvenida al sistema.")

st.info("Selecciona una sección en el menú lateral.")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Módulos", "3")

with col2:
    st.metric("Estado", "Activo")

with col3:
    st.metric("Meta", "Titularme 🎓")

st.markdown("---")

st.write("Secciones disponibles:")

st.write("Electronica")
st.write("Horarios UNAQ")
