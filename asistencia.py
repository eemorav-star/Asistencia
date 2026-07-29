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

# Aplicar estilos globales para todos los botones
st.markdown("""
<style>
    /* Estilo para botón Presente cuando está activo */
    .stButton button[kind="secondary"] {
        transition: all 0.3s ease !important;
    }
    
    /* Estilo para el botón Presente activo */
    button[data-testid="baseButton-secondary"] {
        background-color: #e0e0e0 !important;
        color: #333333 !important;
        border: 2px solid #cccccc !important;
    }
    
    /* Estilo específico para botones Presente activos */
    button[data-testid="baseButton-secondary"]:has(> div:contains("Presente")) {
        background-color: #A4DE02 !important;
        color: black !important;
        border: 2px solid #A4DE02 !important;
        font-weight: bold !important;
        transform: scale(1.05) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    }
    
    /* Estilo específico para botones Tardanza activos */
    button[data-testid="baseButton-secondary"]:has(> div:contains("Tardanza")) {
        background-color: #008CFF !important;
        color: white !important;
        border: 2px solid #008CFF !important;
        font-weight: bold !important;
        transform: scale(1.05) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    }
    
    /* Hover effects */
    button[data-testid="baseButton-secondary"]:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

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
        
        # Botón Presente
        if st.button("Presente", key=f"P_{numero}_{grupo}"):
            st.session_state.Asistencias[numero] = "Presente"
            st.rerun()
        
        # Aplicar estilo específico al botón Presente si está activo
        if estado_actual == "Presente":
            # Usamos JavaScript para cambiar el estilo directamente
            st.markdown(f"""
            <script>
                (function() {{
                    var buttons = document.querySelectorAll('button');
                    for(var i = 0; i < buttons.length; i++) {{
                        if(buttons[i].innerText.trim() === 'Presente' && buttons[i].id.includes('P_{numero}_{grupo}')) {{
                            buttons[i].style.backgroundColor = '#A4DE02';
                            buttons[i].style.color = 'black';
                            buttons[i].style.borderColor = '#A4DE02';
                            buttons[i].style.fontWeight = 'bold';
                            buttons[i].style.transform = 'scale(1.05)';
                            buttons[i].style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
                            buttons[i].style.border = '2px solid #A4DE02';
                            buttons[i].style.transition = 'all 0.3s ease';
                        }}
                    }}
                }})();
            </script>
            """, unsafe_allow_html=True)

    with col4:
        # Obtener el estado actual del estudiante
        estado_actual = st.session_state.Asistencias[numero]
        
        # Botón Tardanza
        if st.button("Tardanza", key=f"T_{numero}_{grupo}"):
            st.session_state.Asistencias[numero] = "Tardanza"
            st.rerun()
        
        # Aplicar estilo específico al botón Tardanza si está activo
        if estado_actual == "Tardanza":
            st.markdown(f"""
            <script>
                (function() {{
                    var buttons = document.querySelectorAll('button');
                    for(var i = 0; i < buttons.length; i++) {{
                        if(buttons[i].innerText.trim() === 'Tardanza' && buttons[i].id.includes('T_{numero}_{grupo}')) {{
                            buttons[i].style.backgroundColor = '#008CFF';
                            buttons[i].style.color = 'white';
                            buttons[i].style.borderColor = '#008CFF';
                            buttons[i].style.fontWeight = 'bold';
                            buttons[i].style.transform = 'scale(1.05)';
                            buttons[i].style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
                            buttons[i].style.border = '2px solid #008CFF';
                            buttons[i].style.transition = 'all 0.3s ease';
                        }}
                    }}
                }})();
            </script>
            """, unsafe_allow_html=True)

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
