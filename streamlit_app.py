import streamlit as st
import json
import os
from datetime import date

st.set_page_config(
    page_title="Rumbo a mi titulación",
    layout="wide"
)

# =========================
# FONDO GALAXIA
# =========================
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
        color: white;
    }

    h1, h2, h3, h4, h5, h6, p, label, div, span {
        color: white !important;
    }

    .stButton>button {
        background-color: #4b5cff;
        color: white;
        border-radius: 12px;
        border: none;
        padding: 0.5rem 1rem;
    }

    .stButton>button:hover {
        background-color: #7b61ff;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# CONFIGURACIÓN
# =========================
DATA_FILE = "data/cursos_main.json"

ESTADOS = [
    "No iniciado",
    "Iniciado",
    "A medias",
    "Casi terminado",
    "Finalizado",
    "Acreditado"
]

DIAS = [
    "Lunes",
    "Martes",
    "Miércoles",
    "Jueves",
    "Viernes",
    "Sábado",
    "Domingo"
]


# =========================
# FUNCIONES
# =========================
def cargar_datos():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(DATA_FILE):
        datos_iniciales = {
            "cursos": [],
            "horario": {dia: [] for dia in DIAS}
        }

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(datos_iniciales, f, indent=4, ensure_ascii=False)

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        datos = json.load(f)

    if "cursos" not in datos:
        datos["cursos"] = []

    if "horario" not in datos:
        datos["horario"] = {dia: [] for dia in DIAS}

    for dia in DIAS:
        if dia not in datos["horario"]:
            datos["horario"][dia] = []

    return datos


def guardar_datos(datos):
    os.makedirs("data", exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


def calcular_progreso_general(cursos):
    if len(cursos) == 0:
        return 0

    total = sum(curso.get("avance", 0) for curso in cursos)
    return int(total / len(cursos))


# =========================
# CARGAR DATOS
# =========================
datos = cargar_datos()

# =========================
# PORTADA
# =========================
st.title("🎓 Camino hacia titularme")
st.subheader("Cursos, acreditaciones, horario y progreso de electrónica")

progreso_general = calcular_progreso_general(datos["cursos"])

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Cursos registrados", len(datos["cursos"]))

with col2:
    st.metric("Progreso general", f"{progreso_general}%")

with col3:
    acreditados = sum(
        1 for curso in datos["cursos"]
        if curso.get("estado") == "Acreditado"
    )
    st.metric("Acreditados", acreditados)

st.progress(progreso_general / 100)

st.divider()

menu = st.radio(
    "Selecciona una sección:",
    [
        "📚 Ver cursos",
        "➕ Agregar curso",
        "🗓️ Mi horario"
    ],
    horizontal=True
)

st.divider()

# =========================
# VER CURSOS
# =========================
if menu == "📚 Ver cursos":
    st.header("📚 Mis cursos y acreditaciones")

    if len(datos["cursos"]) == 0:
        st.info("Todavía no tienes cursos agregados.")
    else:
        filtro = st.selectbox(
            "Filtrar por estado:",
            ["Todos"] + ESTADOS
        )

        for i, curso in enumerate(datos["cursos"]):
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

                    st.write(f"**Estado:** {curso.get('estado', 'No iniciado')}")
                    st.write(f"**Avance:** {curso.get('avance', 0)}%")
                    st.progress(curso.get("avance", 0) / 100)

                    st.write(f"**Precio:** ${curso.get('precio', 0)}")
                    st.write(f"**Días:** {', '.join(curso.get('dias', []))}")
                    st.write(f"**Fecha de inicio:** {curso.get('fecha_inicio', '')}")
                    st.write(f"**Fecha de finalización:** {curso.get('fecha_fin', '')}")

                    with st.expander("✏️ Actualizar curso"):
                        nuevo_estado = st.selectbox(
                            "Estado:",
                            ESTADOS,
                            index=ESTADOS.index(curso.get("estado", "No iniciado")),
                            key=f"estado_{i}"
                        )

                        nuevo_avance = st.slider(
                            "Avance manual:",
                            0,
                            100,
                            int(curso.get("avance", 0)),
                            key=f"avance_{i}"
                        )

                        nuevo_precio = st.number_input(
                            "Precio:",
                            min_value=0.0,
                            value=float(curso.get("precio", 0)),
                            step=50.0,
                            key=f"precio_{i}"
                        )

                        nuevos_dias = st.multiselect(
                            "Días que tomas el curso:",
                            DIAS,
                            default=curso.get("dias", []),
                            key=f"dias_{i}"
                        )

                        nueva_fecha_inicio = st.date_input(
                            "Fecha de inicio:",
                            value=date.fromisoformat(curso.get("fecha_inicio")),
                            key=f"inicio_{i}"
                        )

                        nueva_fecha_fin = st.date_input(
                            "Fecha de finalización:",
                            value=date.fromisoformat(curso.get("fecha_fin")),
                            key=f"fin_{i}"
                        )

                        nuevo_link = st.text_input(
                            "Link del curso:",
                            value=curso.get("link", ""),
                            key=f"link_{i}"
                        )

                        nueva_imagen = st.text_input(
                            "Link de imagen:",
                            value=curso.get("imagen", ""),
                            key=f"imagen_{i}"
                        )

                        if st.button("💾 Guardar cambios", key=f"guardar_{i}"):
                            datos["cursos"][i]["estado"] = nuevo_estado
                            datos["cursos"][i]["avance"] = nuevo_avance
                            datos["cursos"][i]["precio"] = nuevo_precio
                            datos["cursos"][i]["dias"] = nuevos_dias
                            datos["cursos"][i]["fecha_inicio"] = str(nueva_fecha_inicio)
                            datos["cursos"][i]["fecha_fin"] = str(nueva_fecha_fin)
                            datos["cursos"][i]["link"] = nuevo_link
                            datos["cursos"][i]["imagen"] = nueva_imagen

                            guardar_datos(datos)
                            st.success("Curso actualizado correctamente.")
                            st.rerun()

                        if st.button("🗑️ Eliminar curso", key=f"eliminar_{i}"):
                            datos["cursos"].pop(i)
                            guardar_datos(datos)
                            st.warning("Curso eliminado.")
                            st.rerun()


# =========================
# AGREGAR CURSO
# =========================
elif menu == "➕ Agregar curso":
    st.header("➕ Agregar nuevo curso")

    with st.form("form_agregar_curso"):
        nombre = st.text_input("Nombre del curso o acreditación:")

        link = st.text_input("Link del curso:")

        imagen = st.text_input(
            "Link de imagen:",
            placeholder="Pega aquí una URL de imagen"
        )

        estado = st.selectbox("Estado:", ESTADOS)

        avance = st.slider("Avance manual:", 0, 100, 0)

        precio = st.number_input(
            "Precio del curso:",
            min_value=0.0,
            step=50.0
        )

        dias = st.multiselect(
            "Días que tomas el curso:",
            DIAS
        )

        fecha_inicio = st.date_input("Fecha de inicio:")

        fecha_fin = st.date_input("Fecha de finalización:")

        descripcion = st.text_area("Descripción / notas:")

        enviar = st.form_submit_button("➕ Agregar curso")

        if enviar:
            if nombre.strip() == "":
                st.error("Escribe el nombre del curso.")
            else:
                nuevo_curso = {
                    "nombre": nombre,
                    "link": link,
                    "imagen": imagen,
                    "estado": estado,
                    "avance": avance,
                    "precio": precio,
                    "dias": dias,
                    "fecha_inicio": str(fecha_inicio),
                    "fecha_fin": str(fecha_fin),
                    "descripcion": descripcion
                }

                datos["cursos"].append(nuevo_curso)
                guardar_datos(datos)

                st.success("Curso agregado correctamente.")
                st.rerun()


# =========================
# HORARIO
# =========================
elif menu == "🗓️ Mi horario":
    st.header("🗓️ Mi horario")

    dia_seleccionado = st.selectbox(
        "Selecciona un día:",
        DIAS
    )

    st.subheader(f"Horario de {dia_seleccionado}")

    actividades = datos["horario"][dia_seleccionado]

    if len(actividades) == 0:
        st.info("No hay actividades registradas para este día.")

    for i, actividad in enumerate(actividades):
        with st.container(border=True):
            st.write(f"**Hora:** {actividad.get('hora', '')}")
            st.write(f"**Actividad:** {actividad.get('actividad', '')}")
            st.write(f"**Descripción:** {actividad.get('descripcion', '')}")

            if actividad.get("link"):
                st.markdown(f"[🔗 Abrir link]({actividad['link']})")

            with st.expander("✏️ Editar actividad"):
                nueva_hora = st.text_input(
                    "Hora:",
                    value=actividad.get("hora", ""),
                    key=f"hora_{dia_seleccionado}_{i}"
                )

                nueva_actividad = st.text_input(
                    "Actividad:",
                    value=actividad.get("actividad", ""),
                    key=f"actividad_{dia_seleccionado}_{i}"
                )

                nueva_descripcion = st.text_area(
                    "Descripción:",
                    value=actividad.get("descripcion", ""),
                    key=f"descripcion_{dia_seleccionado}_{i}"
                )

                nuevo_link = st.text_input(
                    "Link:",
                    value=actividad.get("link", ""),
                    key=f"link_horario_{dia_seleccionado}_{i}"
                )

                if st.button("💾 Guardar actividad", key=f"guardar_act_{dia_seleccionado}_{i}"):
                    datos["horario"][dia_seleccionado][i] = {
                        "hora": nueva_hora,
                        "actividad": nueva_actividad,
                        "descripcion": nueva_descripcion,
                        "link": nuevo_link
                    }

                    guardar_datos(datos)
                    st.success("Actividad actualizada.")
                    st.rerun()

                if st.button("🗑️ Eliminar actividad", key=f"eliminar_act_{dia_seleccionado}_{i}"):
                    datos["horario"][dia_seleccionado].pop(i)
                    guardar_datos(datos)
                    st.warning("Actividad eliminada.")
                    st.rerun()

    st.divider()

    st.subheader("➕ Agregar actividad al horario")

    with st.form("form_horario"):
        hora = st.text_input("Hora:", placeholder="Ejemplo: 4:00 pm - 6:00 pm")
        actividad = st.text_input("Actividad:", placeholder="Ejemplo: Curso de electrónica")
        descripcion = st.text_area("Descripción:")
        link = st.text_input("Link:")

        agregar_actividad = st.form_submit_button("➕ Agregar actividad")

        if agregar_actividad:
            if actividad.strip() == "":
                st.error("Escribe una actividad.")
            else:
                nueva_actividad = {
                    "hora": hora,
                    "actividad": actividad,
                    "descripcion": descripcion,
                    "link": link
                }

                datos["horario"][dia_seleccionado].append(nueva_actividad)
                guardar_datos(datos)

                st.success("Actividad agregada al horario.")
                st.rerun()
