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
# CSS para estilos profesionales
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

def aplicar_estilos():
    st.markdown("""
    <style>
        /* Estilo para el contenedor de radio buttons */
        .stRadio > div {
            display: flex;
            flex-direction: row;
            gap: 8px;
            flex-wrap: wrap;
        }
        
        /* Ocultar el label del radio */
        .stRadio label {
            display: none !important;
        }
        
        /* Estilo para los radio buttons */
        .stRadio > div > label {
            display: inline-block !important;
            padding: 6px 16px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid #e0e0e0;
            background-color: #f5f5f5;
            color: #555555;
            margin: 2px;
            min-width: 80px;
            text-align: center;
        }
        
        /* Efecto hover */
        .stRadio > div > label:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        /* Estilo para boton seleccionado - Presente */
        .stRadio > div > label:has(input[value="Presente"]:checked) {
            background-color: #1F77B4 !important;
            color: white !important;
            border-color: #1F77B4 !important;
            transform: scale(1.05);
            box-shadow: 0 4px 12px rgba(31, 119, 180, 0.3);
        }
        
        /* Estilo para boton seleccionado - Tardanza */
        .stRadio > div > label:has(input[value="Tardanza"]:checked) {
            background-color: #22C55E !important;
            color: white !important;
            border-color: #22C55E !important;
            transform: scale(1.05);
            box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
        }
        
        /* Estilo para boton seleccionado - Ausente */
        .stRadio > div > label:has(input[value="Ausente"]:checked) {
            background-color: #dc3545 !important;
            color: white !important;
            border-color: #dc3545 !important;
            transform: scale(1.05);
            box-shadow: 0 4px 12px rgba(220, 53, 69, 0.3);
        }
        
        /* Mejorar la tabla de vista previa */
        .stDataFrame {
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        /* Mejorar metricas */
        div[data-testid="metric-container"] {
            background-color: #f8f9fa;
            padding: 16px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
    </style>
    """, unsafe_allow_html=True)

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Funcion para crear radio buttons personalizados
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

def crear_selector_asistencia(estudiante_id, estado_actual, grupo):
    """
    Crea un selector de asistencia usando radio buttons con estilo personalizado
    """
    # Opciones de asistencia (sin Justificado)
    opciones = ["Presente", "Tardanza", "Ausente"]
    
    # Crear radio button horizontal
    seleccion = st.radio(
        label=f"Asistencia_{estudiante_id}",
        options=opciones,
        index=opciones.index(estado_actual) if estado_actual in opciones else 0,
        key=f"radio_{estudiante_id}_{grupo}",
        horizontal=True,
        label_visibility="collapsed"
    )
    
    # Actualizar el estado si cambia
    if seleccion != estado_actual:
        st.session_state.Asistencias[estudiante_id] = seleccion
        st.rerun()
    
    return seleccion

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Interfaz Principal
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

# Aplicar estilos
aplicar_estilos()

st.title("Control de Asistencia - Quinto Año")

# Selector de grupo
col1, col2 = st.columns([1,3])

with col1:
    st.write("**Grupo:**")

with col2:
    grupo = st.radio(
        "Seleccionar Grupo",
        ["A","B","C"],
        index=0 if st.session_state.GrupoSeleccionado=="A"
        else 1 if st.session_state.GrupoSeleccionado=="B"
        else 2,
        horizontal=True,
        label_visibility="collapsed"
    )

if grupo != st.session_state.GrupoSeleccionado:
    CambiarGrupo(grupo)

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
    
    # Crear un contenedor para cada estudiante
    with st.container():
        col1, col2, col3 = st.columns([1, 3, 5])
        
        with col1:
            st.write(f"**{numero}**")
        
        with col2:
            st.write(nombre)
        
        with col3:
            # Selector de asistencia con radio buttons
            crear_selector_asistencia(numero, estado_actual, st.session_state.GrupoSeleccionado)
        
        # Linea separadora sutil
        st.markdown("---")

st.divider()

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Resumen de Asistencia
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

st.subheader("Resumen de Asistencia")

# Contar estados
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

# Mostrar metricas
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Presentes", ContadorPresentes)

with col2:
    st.metric("Tardanzas", ContadorTardanzas)

with col3:
    st.metric("Ausentes", ContadorAusentes)

st.divider()

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Botones de accion
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

col1, col2 = st.columns(2)

with col1:
    if st.button("Guardar Asistencia", use_container_width=True):
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

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Vista previa y descarga
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

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
    
    # Boton de descarga
    csv = DfPreview.to_csv(index=False)
    st.download_button(
        label="Descargar CSV",
        data=csv,
        file_name=f"asistencia_grupo_{st.session_state.GrupoSeleccionado}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )
