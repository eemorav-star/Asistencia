#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Universidad Tecnologica de Panama
# Semestral de Herramientas de programacion 1
# Integrantes: Jaen Kathya, Luna Adrian, Mora Elpidio
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

import streamlit as st
import pandas as pd
from datetime import datetime
from grupos import GrupoA,Grupos
from exc import GuardarAsistencia

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Inicializar estado de la sesion
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

if "GrupoSeleccionado" not in st.session_state:
    st.session_state.GrupoSeleccionado = "A"

if "EstudiantesActuales" not in st.session_state:
    st.session_state.EstudiantesActuales = GrupoA

if "Asistencias" not in st.session_state:

    st.session_state.Asistencias = {}

    for estudiante in GrupoA:

        st.session_state.Asistencias[estudiante["numero"]] = "Ausente"

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Funcion para cambiar de grupo
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

def CambiarGrupo(grupo):

    st.session_state.EstudiantesActuales = Grupos[grupo]

    st.session_state.Asistencias = {}

    for estudiante in st.session_state.EstudiantesActuales:

        st.session_state.Asistencias[estudiante["numero"]] = "Ausente"

    st.session_state.GrupoSeleccionado = grupo

    st.rerun()

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Funcion para aplicar estilos a los botones
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

def boton_con_estilo(texto, key, color_activo, color_inactivo, estado_actual, estado_deseado):
    """
    Crea un botón con estilo que cambia de color según el estado
    """
    # Determinar si el botón debe estar activo
    es_activo = (estado_actual == estado_deseado)
    
    # Seleccionar el color según el estado
    color_fondo = color_activo if es_activo else color_inactivo
    
    # CSS para el botón
    estilo = f"""
    <style>
    div.stButton > button[data-testid="baseButton-secondary"] {{
        background-color: {color_fondo} !important;
        color: {'black' if es_activo else 'white'} !important;
        border: 2px solid {color_fondo} !important;
        transition: all 0.3s ease !important;
        font-weight: bold !important;
    }}
    div.stButton > button[data-testid="baseButton-secondary"]:hover {{
        transform: scale(1.05) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
        background-color: {color_activo} !important;
        color: {'black' if estado_deseado == "Presente" else 'white'} !important;
    }}
    </style>
    """
    
    # Aplicar el estilo
    st.markdown(estilo, unsafe_allow_html=True)
    
    # Crear el botón
    return st.button(texto, key=key)

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Interfaz
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

st.title("Control de Asistencia - Quinto Año")

col1, col2 = st.columns([1,3])

with col1:

    st.write("**Seleccionar Grupo:**")

with col2:

    grupo = st.radio(

        "Grupo",

        ["A","B","C"],

        index=0 if st.session_state.GrupoSeleccionado=="A"
        else 1 if st.session_state.GrupoSeleccionado=="B"
        else 2,

        horizontal=True

    )

if grupo != st.session_state.GrupoSeleccionado:

    CambiarGrupo(grupo)

st.write(
    f"**Grupo {st.session_state.GrupoSeleccionado} - "
    f"{len(st.session_state.EstudiantesActuales)} estudiantes**"
)

FechaHora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

st.write(f"**Fecha y Hora:** {FechaHora}")

st.divider()

st.subheader("Registro de Asistencia")

for estudiante in st.session_state.EstudiantesActuales:

    numero = estudiante["numero"]

    nombre = estudiante["nombre"]

    col1,col2,col3,col4 = st.columns([1,4,1,1])

    with col1:

        st.write(numero)

    with col2:

        st.write(nombre)

    with col3:
        # Obtener el estado actual del estudiante
        estado_actual = st.session_state.Asistencias[numero]
        
        # Botón Presente con estilo verde lima (#A4DE02)
        if st.button("Presente", key=f"P_{numero}_{grupo}"):
            st.session_state.Asistencias[numero] = "Presente"
            st.rerun()
        
        # Aplicar estilo al botón Presente
        if estado_actual == "Presente":
            st.markdown(
                f"""
                <style>
                div[data-testid="column"]:nth-child(3) button {{
                    background-color: #A4DE02 !important;
                    color: black !important;
                    border: 2px solid #A4DE02 !important;
                    font-weight: bold !important;
                    transform: scale(1.05) !important;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )

    with col4:
        # Obtener el estado actual del estudiante
        estado_actual = st.session_state.Asistencias[numero]
        
        # Botón Tardanza con estilo azul eléctrico (#008CFF)
        if st.button("Tardanza", key=f"T_{numero}_{grupo}"):
            st.session_state.Asistencias[numero] = "Tardanza"
            st.rerun()
        
        # Aplicar estilo al botón Tardanza
        if estado_actual == "Tardanza":
            st.markdown(
                f"""
                <style>
                div[data-testid="column"]:nth-child(4) button {{
                    background-color: #008CFF !important;
                    color: white !important;
                    border: 2px solid #008CFF !important;
                    font-weight: bold !important;
                    transform: scale(1.05) !important;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )

st.divider()
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Resumen de Asistencia
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

st.subheader("Resumen de Asistencia")

ContadorPresentes = 0
ContadorTardanzas = 0
ContadorAusentes = 0

i = 0

while i < len(st.session_state.EstudiantesActuales):

    numero = st.session_state.EstudiantesActuales[i]["numero"]

    estado = st.session_state.Asistencias[numero]

    if estado == "Presente":

        ContadorPresentes += 1

    elif estado == "Tardanza":

        ContadorTardanzas += 1

    else:

        ContadorAusentes += 1

    i += 1

col1, col2, col3 = st.columns(3)

with col1:

    st.metric("Presentes", ContadorPresentes)

with col2:

    st.metric("Tardanzas", ContadorTardanzas)

with col3:

    st.metric("Ausentes", ContadorAusentes)

st.divider()

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Botones
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

col1, col2 = st.columns(2)

with col1:

    if st.button("Guardar Asistencia"):

        try:

            GuardarAsistencia(

                st.session_state.GrupoSeleccionado,

                st.session_state.EstudiantesActuales,

                st.session_state.Asistencias

            )

            st.success("La asistencia fue guardada correctamente.")

        except Exception as e:

            st.error(f"Error al guardar: {e}")

with col2:

    if st.button("Reiniciar Asistencia"):

        for estudiante in st.session_state.EstudiantesActuales:

            st.session_state.Asistencias[estudiante["numero"]] = "Ausente"

        st.success("Asistencia reiniciada.")

        st.rerun()

VerVistaPrevia = st.checkbox("Ver vista previa antes de descargar")

if VerVistaPrevia:
    FilasPreview = []
    for estudiante in st.session_state.EstudiantesActuales:
        num = estudiante["numero"]
        nombre = estudiante["nombre"]
        estado = st.session_state.Asistencias[num]
        FilasPreview.append({"N°": num, "Nombre": nombre, "Estado": estado})

    DfPreview = pd.DataFrame(FilasPreview)
    st.dataframe(DfPreview, hide_index=True, use_container_width=True)
