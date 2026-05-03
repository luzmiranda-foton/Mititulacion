import streamlit as st
import json
import os
from datetime import date

st.set_page_config(
    page_title="Camino hacia titularme",
    page_icon="🎓",
    layout="wide"
)

DATA_FILE = "data/cursos_main.json"

ESTADOS = [
    "No iniciado",
    "Iniciado",
    "A medias",
    "Casi terminado",
    "Finalizado",
    "Acreditado"
]

DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]


def cargar_datos():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(DATA_FILE):
        datos_iniciales = {"cursos": []}
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(datos_iniciales, f, indent=4, ensure_ascii=False)

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_datos(datos):
    os.makedirs("data", exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


datos = cargar_datos()

st.title("🎓 Camino hacia titularme")
st.subheader("Cursos, acreditaciones y avance en electrónica")

st.divider()

menu = st.radio(
    "Menú:",
    ["📚 Ver cursos", "➕ Agregar curso"],
    horizontal=True
)

# =========================
# VER CURSOS
# =========================
if menu == "📚 Ver cursos":
    st.header("📚 Mis cursos")

    if len(datos["cursos"]) == 0:
        st.info("Todavía no tienes cursos agregados.")
    else:
        for i, curso in enumerate(datos["cursos"]):
            with st.container(border=True):
                col_img, col_info = st.columns([1, 3])

                with col_img:
                    if curso.get("imagen"):
                        st.image(curso["imagen"], use_container_width=True)
                    else:
                        st.info("Sin imagen")

                with col_info:
                    st.subheader(curso["nombre"])

                    if curso.get("link"):
                        st.markdown(f"[Abrir curso]({curso['link']})")

                    st.write(f"**Estado:** {curso['estado']}")
                    st.write(f"**Avance:** {curso['avance']}%")
                    st.progress(curso["avance"] / 100)

                    st.write(f"**Precio:** ${curso['precio']}")
                    st.write(f"**Días:** {', '.join(curso['dias'])}")
                    st.write(f"**Inicio:** {curso['fecha_inicio']}")
                    st.write(f"**Fin:** {curso['fecha_fin']}")

                    with st.expander("✏️ Actualizar curso"):
                        nuevo_estado = st.selectbox(
                            "Estado:",
                            ESTADOS,
                            index=ESTADOS
