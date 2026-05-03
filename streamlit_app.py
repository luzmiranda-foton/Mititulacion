import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import date
import uuid

st.set_page_config(
    page_title="Camino hacia titularme",
    page_icon="🎓",
    layout="wide"
)

SHEET_NAME = "Camino hacia titularme"

ESTADOS = [
    "No iniciado",
    "Iniciado",
    "A medias",
    "Casi terminado",
    "Finalizado",
    "Acreditado"
]

DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]


st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1462331940025-496dfbfc7564");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }

    .block-container {
        background: rgba(0, 0, 0, 0.68);
        padding: 2rem;
        border-radius: 25px;
    }

    .block-container h1,
    .block-container h2,
    .block-container h3,
    .block-container p,
    .block-container label {
        color: white !important;
    }

    input, textarea {
        color: black !important;
        background-color: white !important;
    }

    [data-baseweb="select"] * {
        color: black !important;
    }

    [data-testid="stDateInput"] * {
        color: black !important;
    }

    .stButton>button {
        background-color: #4b5cff;
        color: white !important;
        border-radius: 12px;
        border: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def conectar_sheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        st.secrets["google_service_account"],
        scopes=scopes
    )

    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).sheet1
    return sheet


def cargar_cursos():
    sheet = conectar_sheet()
    return sheet.get_all_records()


def agregar_curso(curso):
    sheet = conectar_sheet()
    sheet.append_row([
        curso["id"],
        curso["nombre"],
        curso["link"],
        curso["imagen"],
        curso["estado"],
        curso["avance"],
        curso["precio"],
        curso["dias"],
        curso["fecha_inicio"],
        curso["fecha_fin"],
        curso["descripcion"]
    ])


def actualizar_curso(fila, curso):
    sheet = conectar_sheet()
    sheet.update(f"A{fila}:K{fila}", [[
        curso["id"],
        curso["nombre"],
        curso["link"],
        curso["imagen"],
        curso["estado"],
        curso["avance"],
        curso["precio"],
        curso["dias"],
        curso["fecha_inicio"],
        curso["fecha_fin"],
        curso["descripcion"]
    ]])


def eliminar_curso(fila):
    sheet = conectar_sheet()
    sheet.delete_rows(fila)


st.title("🎓 Camino hacia titularme")
st.subheader("Cursos, acreditaciones y progreso de electrónica")

try:
    cursos = cargar_cursos()
except Exception as e:
    st.error("No se pudo conectar con Google Sheets.")
    st.write(e)
    st.stop()

progreso_general = 0
if len(cursos) > 0:
    progreso_general = int(sum(int(curso.get("avance", 0)) for curso in cursos) / len(cursos))

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Cursos registrados", len(cursos))

with col2:
    st.metric("Progreso general", f"{progreso_general}%")

with col3:
    acreditados = sum(1 for curso in cursos if curso.get("estado") == "Acreditado")
    st.metric("Acreditados", acreditados)

st.progress(progreso_general / 100)

st.divider()

menu = st.radio(
    "Selecciona una sección:",
    ["📚 Ver cursos", "➕ Agregar curso"],
    horizontal=True
)

st.divider()

if menu == "📚 Ver cursos":
    st.header("📚 Mis cursos")

    if len(cursos) == 0:
        st.info("Todavía no tienes cursos registrados.")
    else:
        filtro = st.selectbox("Filtrar por estado:", ["Todos"] + ESTADOS)

        for i, curso in enumerate(cursos):
            fila_sheet = i + 2

            if filtro != "Todos" and curso.get("estado") != filtro:
                continue

            with st.container(border=True):
                col_img, col_info = st.columns([1, 3])

                with col_img:
                    if curso.get("imagen"):
                        st.image(curso["imagen"], use_container_width=True)
                    else:
                        st.info("Sin imagen")

                with col_info:
                    st.subheader(curso.get("nombre", "Curso sin nombre"))

                    if curso.get("link"):
                        st.markdown(f"[🔗 Abrir curso]({curso['link']})")

                    avance_actual = int(curso.get("avance", 0))

                    st.write(f"**Estado:** {curso.get('estado', 'No iniciado')}")
                    st.write(f"**Avance:** {avance_actual}%")
                    st.progress(avance_actual / 100)
                    st.write(f"**Precio:** ${curso.get('precio', 0)}")
                    st.write(f"**Días:** {curso.get('dias', '')}")
                    st.write(f"**Inicio:** {curso.get('fecha_inicio', '')}")
                    st.write(f"**Fin:** {curso.get('fecha_fin', '')}")
                    st.write(f"**Notas:** {curso.get('descripcion', '')}")

                    with st.expander("✏️ Actualizar curso"):
                        nombre = st.text_input("Nombre:", value=curso.get("nombre", ""), key=f"nombre_{i}")
                        link = st.text_input("Link:", value=curso.get("link", ""), key=f"link_{i}")
                        imagen = st.text_input("Imagen:", value=curso.get("imagen", ""), key=f"imagen_{i}")

                        estado_actual = curso.get("estado", "No iniciado")
                        if estado_actual not in ESTADOS:
                            estado_actual = "No iniciado"

                        estado = st.selectbox(
                            "Estado:",
                            ESTADOS,
                            index=ESTADOS.index(estado_actual),
                            key=f"estado_{i}"
                        )

                        avance = st.slider("Avance:", 0, 100, avance_actual, key=f"avance_{i}")
                        precio = st.number_input("Precio:", min_value=0.0, value=float(curso.get("precio", 0)), key=f"precio_{i}")

                        dias_actuales = curso.get("dias", "")
                        dias_lista = [d.strip() for d in dias_actuales.split(",") if d.strip() in DIAS]

                        dias = st.multiselect("Días:", DIAS, default=dias_lista, key=f"dias_{i}")

                        fecha_inicio = st.text_input("Fecha inicio:", value=curso.get("fecha_inicio", ""), key=f"inicio_{i}")
                        fecha_fin = st.text_input("Fecha fin:", value=curso.get("fecha_fin", ""), key=f"fin_{i}")
                        descripcion = st.text_area("Descripción:", value=curso.get("descripcion", ""), key=f"desc_{i}")

                        if st.button("💾 Guardar cambios", key=f"guardar_{i}"):
                            curso_actualizado = {
                                "id": curso.get("id", str(uuid.uuid4())),
                                "nombre": nombre,
                                "link": link,
                                "imagen": imagen,
                                "estado": estado,
                                "avance": avance,
                                "precio": precio,
                                "dias": ", ".join(dias),
                                "fecha_inicio": fecha_inicio,
                                "fecha_fin": fecha_fin,
                                "descripcion": descripcion
                            }

                            actualizar_curso(fila_sheet, curso_actualizado)
                            st.success("Curso actualizado.")
                            st.rerun()

                        if st.button("🗑️ Eliminar curso", key=f"eliminar_{i}"):
                            eliminar_curso(fila_sheet)
                            st.warning("Curso eliminado.")
                            st.rerun()


elif menu == "➕ Agregar curso":
    st.header("➕ Agregar curso")

    with st.form("form_agregar"):
        nombre = st.text_input("Nombre del curso:")
        link = st.text_input("Link del curso:")
        imagen = st.text_input("Link de imagen:")
        estado = st.selectbox("Estado:", ESTADOS)
        avance = st.slider("Avance:", 0, 100, 0)
        precio = st.number_input("Precio:", min_value=0.0, step=50.0)
        dias = st.multiselect("Días que tomas el curso:", DIAS)
        fecha_inicio = st.date_input("Fecha de inicio:")
        fecha_fin = st.date_input("Fecha de finalización:")
        descripcion = st.text_area("Descripción / notas:")

        enviar = st.form_submit_button("➕ Agregar curso")

        if enviar:
            if nombre.strip() == "":
                st.error("Escribe el nombre del curso.")
            else:
                nuevo_curso = {
                    "id": str(uuid.uuid4()),
                    "nombre": nombre,
                    "link": link,
                    "imagen": imagen,
                    "estado": estado,
                    "avance": avance,
                    "precio": precio,
                    "dias": ", ".join(dias),
                    "fecha_inicio": str(fecha_inicio),
                    "fecha_fin": str(fecha_fin),
                    "descripcion": descripcion
                }

                agregar_curso(nuevo_curso)
                st.success("Curso guardado en Google Sheets.")
                st.rerun()
