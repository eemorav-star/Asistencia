# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Universidad Tecnologica de Panama
# Semestral de Herramientas de programacion 1
# Integrantes: Jaen Kathya, Luna Adrian, Mora Elpidio
# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

import streamlit as st
import pandas as pd
from datetime import datetime
# Nota: Asumo que tienes estos archivos/modulos en tu carpeta
# try/except para evitar errores si no existen al probar solo la interfaz
try:
    from grupos import GrupoA, Grupos
    from exc import GuardarAsistencia
except ImportError:
    # Datos de prueba por si acaso
    GrupoA = [{"numero": "1", "nombre": "Estudiante Prueba 1"}]
    Grupos = {"A": GrupoA, "B": GrupoA, "C": GrupoA}
    def GuardarAsistencia(*args): pass

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
# CSS AVANZADO para forzar colores del círculo
# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

def aplicar_estilos():
    st.markdown("""
    <style>
        /* 1. Contenedor horizontal */
        .stRadio > div {
            display: flex;
            flex-direction: row;
            gap: 10px;
        }
        
        /* 2. Ocultar label principal de Streamlit */
        .stRadio label:not([data-testid="stWidgetLabel"]) {
            display: none !important;
        }
        
        /* 3. Estilo base de los botones (etiquetas) */
        .stRadio div[data-testid="stMarkdownContainer"] > p {
            margin-bottom: 0px; /* Corrección de margen en texto */
        }

        .stRadio > div > label {
            display: inline-flex !important;
            align-items: center;
            justify-content: center;
            padding: 8px 16px;
            border-radius: 20px; /* Más redondeado, estilo píldora */
            border: 1px solid #d1d5db;
            background-color: white;
            cursor: pointer;
            transition: all 0.2s;
            font-weight: 500;
            color: #374151;
        }

        /* Hover general */
        .stRadio > div > label:hover {
            border-color: #9ca3af;
            background-color: #f9fafb;
        }

        /* ========================================================
           ESTILOS CUANDO ESTÁ SELECCIONADO (Checked)
           Forzamos el color del borde y el texto del botón
           ======================================================== */

        /* PRESENTE -> Azul */
        .stRadio > div > label:has(input[value="Presente"]:checked) {
            border-color: #1E40AF !important; /* Azul oscuro */
            background-color: #EFF6FF !important; /* Azul muy pálido */
            color: #1E40AF !important;
        }

        /* TARDANZA -> Verde */
        .stRadio > div > label:has(input[value="Tardanza"]:checked) {
            border-color: #166534 !important; /* Verde oscuro */
            background-color: #F0FDF4 !important; /* Verde muy pálido */
            color: #166534 !important;
        }

        /* AUSENTE -> Rojo */
        .stRadio > div > label:has(input[value="Ausente"]:checked) {
            border-color: #B91C1C !important; /* Rojo oscuro */
            background-color: #FEF2F2 !important; /* Rojo muy pálido */
            color: #B91C1C !important;
        }

        /* ========================================================
           SOLUCIÓN DEFINITIVA PARA EL PUNTO INTERIOR
           Apuntamos a los pseudo-elementos que Streamlit usa para dibujar el radio
           ======================================================== */
        
        /* Base del círculo exterior del radio button (por defecto gris) */
        .stRadio input[type="radio"] + div[data-testid="stRadioButtonCustomObject"] {
            border-color: #d1d5db !important;
        }

        /* --- Colores del punto interior cuando está CHECKED --- */

        /* 1. PRESENTE -> PUNTO AZUL */
        .stRadio > div > label:has(input[value="Presente"]:checked) input[type="radio"] + div[data-testid="stRadioButtonCustomObject"]::after {
            background-color: #1E40AF !important; /* Azul */
            transform: scale(1) !important; /* Forzar visibilidad */
        }
        /* Círculo exterior azul al seleccionar Presente */
        .stRadio > div > label:has(input[value="Presente"]:checked) input[type="radio"] + div[data-testid="stRadioButtonCustomObject"] {
            border-color: #1E40AF !important;
        }

        /* 2. TARDANZA -> PUNTO VERDE */
        .stRadio > div > label:has(input[value="Tardanza"]:checked) input[type="radio"] + div[data-testid="stRadioButtonCustomObject"]::after {
            background-color: #166534 !important; /* Verde */
            transform: scale(1) !important;
        }
        /* Círculo exterior verde al seleccionar Tardanza */
        .stRadio > div > label:has(input[value="Tardanza"]:checked) input[type="radio"] + div[data-testid="stRadioButtonCustomObject"] {
            border-color: #166534 !important;
        }

        /* 3. AUSENTE -> PUNTO ROJO */
        .stRadio > div > label:has(input[value="Ausente"]:checked) input[type="radio"] + div[data-testid="stRadioButtonCustomObject"]::after {
            background-color: #B91C1C !important; /* Rojo */
            transform: scale(1) !important;
        }
        /* Círculo exterior rojo al seleccionar Ausente */
        .stRadio > div > label:has(input[value="Ausente"]:checked) input[type="radio"] + div[data-testid="stRadioButtonCustomObject"] {
            border-color: #B91C1C !important;
        }

        /* --- Estilos extra para metricas y tabla --- */
        div[data-testid="metric-container"] {
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 10px;
            border: 1px solid #e9ecef;
        }
    </style>
    """, unsafe_allow_html=True)

# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Funcion para crear radio buttons personalizados
# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

def crear_selector_asistencia(estudiante_id, estado_actual, grupo):
    """
    Crea un selector de asistencia usando radio buttons
    """
    opciones = ["Presente", "Tardanza", "Ausente"]
    
    seleccion = st.radio(
        label=f"Asistencia_{estudiante_id}",
        options=opciones,
        index=opciones.index(estado_actual) if estado_actual in opciones else 0,
        key=f"radio_{estudiante_id}_{grupo}",
        horizontal=True,
        label_visibility="collapsed"
    )
    
    if seleccion != estado_actual:
        st.session_state.Asistencias[estudiante_id] = seleccion
        st.rerun()
    
    return seleccion

# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Interfaz Principal
# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

# Aplicar estilos CSS avanzados
aplicar_estilos()

st.title("Control de Asistencia - Quinto Año")

# Selector de grupo
col1, col2 = st.columns([1, 3])

with col1:
    st.write("**Grupo:**")

with col2:
    grupo = st.radio(
        "Seleccionar Grupo",
        ["A", "B", "C"],
        index=0 if st.session_state.GrupoSeleccionado == "A"
        else 1 if st.session_state.GrupoSeleccionado == "B"
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
    
    with st.container():
        # Ajuste leve de columnas para que quepa mejor el texto
        col1, col2, col3 = st.columns([1, 4, 6])
        
        with col1:
            st.write(f"**{numero}**")
        
        with col2:
            st.write(nombre)
        
        with col3:
            # Selector de asistencia
            crear_selector_asistencia(numero, estado_actual, st.session_state.GrupoSeleccionado)
        
        st.markdown("<div style='margin-top:-15px'></div>", unsafe_allow_html=True) # Reducir espacio
        st.divider()

# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Resumen de Asistencia
# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

st.divider()
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
