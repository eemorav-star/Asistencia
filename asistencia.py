#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Universidad Tecnologica de Panama
# Semestral de Herramientas de programacion 1
# Integrantes: Jaen Kathya, Luna Adrian, Mora Elpidio
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

import streamlit as st
import pandas as pd
from datetime import datetime
from grupos import GrupoA, Grupos
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
# Procesar acciones de los botones via query params
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

query_params = st.query_params
accion = query_params.get("accion", None)
estudiante_id = query_params.get("estudiante", None)
grupo_param = query_params.get("grupo", None)

if accion and estudiante_id and grupo_param:
    if accion == "presente":
        st.session_state.Asistencias[estudiante_id] = "Presente"
    elif accion == "tardanza":
        st.session_state.Asistencias[estudiante_id] = "Tardanza"
    # Limpiar query params y recargar
    st.query_params.clear()
    st.rerun()

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
# Funcion para crear botones HTML con estilo
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

def crear_boton_personalizado(texto, estudiante_id, grupo, estado_actual, tipo):
    """
    Crea un botón HTML personalizado con estilo dinámico
    tipo: 'presente' o 'tardanza'
    """
    if tipo == "presente":
        color_activo = "#A4DE02"
        color_inactivo = "#e0e0e0"
        texto_color_activo = "black"
        texto_color_inactivo = "#333333"
        es_activo = (estado_actual == "Presente")
        accion_url = "presente"
    else:  # tardanza
        color_activo = "#008CFF"
        color_inactivo = "#e0e0e0"
        texto_color_activo = "white"
        texto_color_inactivo = "#333333"
        es_activo = (estado_actual == "Tardanza")
        accion_url = "tardanza"
    
    color_fondo = color_activo if es_activo else color_inactivo
    color_texto = texto_color_activo if es_activo else texto_color_inactivo
    borde = color_activo if es_activo else "#cccccc"
    escala = "scale(1.05)" if es_activo else "scale(1)"
    sombra = "0 4px 8px rgba(0,0,0,0.2)" if es_activo else "none"
    
    html_boton = f'''
    <button 
        onclick="window.location.href='?accion={accion_url}&estudiante={estudiante_id}&grupo={grupo}'" 
        style="
            background-color: {color_fondo};
            color: {color_texto};
            border: 2px solid {borde};
            padding: 8px 16px;
            border-radius: 8px;
            font-weight: bold;
            width: 100%;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 14px;
            transform: {escala};
            box-shadow: {sombra};
            font-family: 'Source Sans Pro', sans-serif;
            margin: 2px 0;
        "
        onmouseover="this.style.transform='scale(1.05)';this.style.boxShadow='0 4px 8px rgba(0,0,0,0.2)'"
        onmouseout="this.style.transform='{escala}';this.style.boxShadow='{sombra}'"
    >
        {texto}
    </button>
    '''
    return html_boton

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
    estado_actual = st.session_state.Asistencias[numero]

    col1, col2, col3, col4 = st.columns([1,4,1,1])

    with col1:
        st.write(numero)

    with col2:
        st.write(nombre)

    with col3:
        # Botón Presente personalizado
        html_presente = crear_boton_personalizado(
            "Presente", numero, st.session_state.GrupoSeleccionado, 
            estado_actual, "presente"
        )
        st.markdown(html_presente, unsafe_allow_html=True)

    with col4:
        # Botón Tardanza personalizado
        html_tardanza = crear_boton_personalizado(
            "Tardanza", numero, st.session_state.GrupoSeleccionado, 
            estado_actual, "tardanza"
        )
        st.markdown(html_tardanza, unsafe_allow_html=True)

st.divider()

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Resumen de Asistencia
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

st.subheader("Resumen de Asistencia")

ContadorPresentes = 0
ContadorTardanzas = 0
ContadorAusentes = 0

for estudiante in st.session_state.EstudiantesActuales:
    estado = st.session_state.Asistencias[estudiante["numero"]]
    if estado == "Presente":
        ContadorPresentes += 1
    elif estado == "Tardanza":
        ContadorTardanzas += 1
    else:
        ContadorAusentes += 1

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Presentes", ContadorPresentes)

with col2:
    st.metric("Tardanzas", ContadorTardanzas)

with col3:
    st.metric("Ausentes", ContadorAusentes)

st.divider()

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Botones de acción
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
