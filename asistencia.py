# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Universidad Tecnologica de Panama
# Semestral de Herramientas de programacion 1
# Integrantes: Jaen Kathya, Luna Adrian, Mora Elpidio
# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

import streamlit as st
import pandas as pd
from datetime import datetime
from grupos import GrupoA, Grupos
from exc import GuardarAsistencia

# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Inicializar estado de la sesion
# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

if "GrupoSeleccionado" not in st.session_state:
    st.session_state.GrupoSeleccionado = "A"

if "EstudiantesActuales" not in st.session_state:
    st.session_state.EstudiantesActuales = GrupoA

if "Asistencias" not in st.session_state:
    st.session_state.Asistencias = {}
    for estudiante in GrupoA:
        st.session_state.Asistencias[estudiante["numero"]] = "Ausente"

# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Funcion para cambiar de grupo
# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

def CambiarGrupo(grupo):
    st.session_state.EstudiantesActuales = Grupos[grupo]
    st.session_state.Asistencias = {}
    for estudiante in st.session_state.EstudiantesActuales:
        st.session_state.Asistencias[estudiante["numero"]] = "Ausente"
    st.session_state.GrupoSeleccionado = grupo
    st.rerun()

# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# CSS para estilos generales de la interfaz
# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

def aplicar_estilos():
    st.markdown("""
    <style>
        /* Estilos para la tabla de vista previa */
        .stDataFrame {
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        /* Estilos para las tarjetas de métricas */
        div[data-testid="metric-container"] {
            background-color: #f8f9fa;
            padding: 16px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
    </style>
    """, unsafe_allow_html=True)

# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Funcion para crear selector de asistencia con botones dinamicos
# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

def crear_selector_asistencia(estudiante_id, estado_actual, grupo):
    col1, col2, col3 = st.columns(3)

    # Colores según el estado seleccionado:
    # Presente -> Azul (#1F77B4), Tardanza -> Verde (#22C55E), Ausente -> Rojo (#DC3545)
    color_presente = "#1F77B4" if estado_actual == "Presente" else "#F1F3F4"
    color_tardanza = "#22C55E" if estado_actual == "Tardanza" else "#F1F3F4"
    color_ausente  = "#DC3545" if estado_actual == "Ausente" else "#F1F3F4"

    # Estilos dinámicos para los tres botones de este estudiante
    st.markdown(f"""
    <style>
    div[data-testid="stHorizontalBlock"] button {{
        font-weight: bold;
        border-radius: 8px;
        height: 40px;
        border: 1px solid #d1d5db;
        transition: all 0.2s ease;
    }}

    div[data-testid="stHorizontalBlock"] > div:nth-child(1) button {{
        background-color: {color_presente} !important;
        color: {"white" if estado_actual == "Presente" else "#333333"} !important;
        border-color: {"#1F77B4" if estado_actual == "Presente" else "#d1d5db"} !important;
    }}

    div[data-testid="stHorizontalBlock"] > div:nth-child(2) button {{
        background-color: {color_tardanza} !important;
        color: {"white" if estado_actual == "Tardanza" else "#333333"} !important;
        border-color: {"#22C55E" if estado_actual == "Tardanza" else "#d1d5db"} !important;
    }}

    div[data-testid="stHorizontalBlock"] > div:nth-child(3) button {{
        background-color: {color_ausente} !important;
        color: {"white" if estado_actual == "Ausente" else "#333333"} !important;
        border-color: {"#DC3545" if estado_actual == "Ausente" else "#d1d5db"} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    with col1:
        if st.button("Presente", key=f"P_{estudiante_id}_{grupo}", use_container_width=True):
            st.session_state.Asistencias[estudiante_id] = "Presente"
            st.rerun()

    with col2:
        if st.button("Tardanza", key=f"T_{estudiante_id}_{grupo}", use_container_width=True):
            st.session_state.Asistencias[estudiante_id] = "Tardanza"
            st.rerun()

    with col3:
        if st.button("Ausente", key=f"A_{estudiante_id}_{grupo}", use_container_width=True):
            st.session_state.Asistencias[estudiante_id] = "Ausente"
            st.rerun()

# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Interfaz Principal
# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

aplicar_estilos()

st.title("Control de Asistencia - Quinto Año")

# Selector de grupo usando st.segmented_control (o botones si se prefiere)
col1, col2 = st.columns([1, 3])

with col1:
    st.write("**Grupo:**")

with col2:
    grupo_sel = st.radio(
        "Seleccionar Grupo",
        ["A", "B", "C"],
        index=0 if st.session_state.GrupoSeleccionado == "A"
        else 1 if st.session_state.GrupoSeleccionado == "B"
        else 2,
        horizontal=True,
        label_visibility="collapsed"
    )

if grupo_sel != st.session_state.GrupoSeleccionado:
    CambiarGrupo(grupo_sel)

# Informacion del grupo
st.write(
    f"**Grupo {st.session_state.GrupoSeleccionado} - "
    f"{len(st.session_state.EstudiantesActuales)} estudiantes**"
)

FechaHora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
st.write(f"**Fecha y Hora:** {FechaHora}")

st.divider()

st.subheader("Registro de Asistencia")

# Lista de estudiantes
for estudiante in st.session_state.EstudiantesActuales:
    numero = estudiante["numero"]
    nombre = estudiante["nombre"]
    estado_actual = st.session_state.Asistencias[numero]
    
    with st.container():
        col1, col2, col3 = st.columns([1, 3, 5])
        
        with col1:
            st.write(f"**{numero}**")
        
        with col2:
            st.write(nombre)
        
        with col3:
            # Reutilizando exactamente la misma firma de llamada
            crear_selector_asistencia(
                numero,
                estado_actual,
                st.session_state.GrupoSeleccionado
            )
        
        st.markdown("---")

st.divider()

# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Resumen de Asistencia
# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

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

# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Botones de accion
# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

col1, col2 = st.columns(2)

with col1:
    if st.button("Guardar Asistencia", use_container_width=True, type="primary"):
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
    if st.button("Reiniciar Asistencia", use_container_width=True):
        for estudiante in st.session_state.EstudiantesActuales:
            st.session_state.Asistencias[estudiante["numero"]] = "Ausente"
        st.success("Asistencia reiniciada.")
        st.rerun()

st.divider()

# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Vista previa y descarga
# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

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
    
    csv = DfPreview.to_csv(index=False)
    st.download_button(
        label="Descargar CSV",
        data=csv,
        file_name=f"asistencia_grupo_{st.session_state.GrupoSeleccionado}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )
