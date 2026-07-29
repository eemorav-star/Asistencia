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
    elif accion == "ausente":
        st.session_state.Asistencias[estudiante_id] = "Ausente"
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
# Funcion para crear botones con estilo usando components
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

def crear_boton_asistencia(texto, estudiante_id, grupo, estado_actual, tipo):
    """
    Crea un boton HTML con estilo dinamico usando st.components
    tipo: 'presente', 'tardanza', o 'ausente'
    """
    # Configurar colores segun tipo
    if tipo == "presente":
        color_activo = "#1F77B4"  # Azul
        es_activo = (estado_actual == "Presente")
        accion = "presente"
    elif tipo == "tardanza":
        color_activo = "#22C55E"  # Verde
        es_activo = (estado_actual == "Tardanza")
        accion = "tardanza"
    else:  # ausente
        color_activo = "#dc3545"  # Rojo
        es_activo = (estado_actual == "Ausente")
        accion = "ausente"
    
    # Determinar colores segun estado
    if es_activo:
        bg_color = color_activo
        text_color = "white"
        border_color = color_activo
        transform = "scale(1.05)"
        shadow = "0 4px 12px rgba(0,0,0,0.2)"
        font_weight = "700"
    else:
        bg_color = "#f3f4f6"
        text_color = "#6b7280"
        border_color = "#d1d5db"
        transform = "scale(1)"
        shadow = "none"
        font_weight = "500"
    
    html = f'''
    <button 
        onclick="window.location.href='?accion={accion}&estudiante={estudiante_id}&grupo={grupo}'" 
        style="
            background-color: {bg_color};
            color: {text_color};
            border: 2px solid {border_color};
            padding: 6px 18px;
            border-radius: 20px;
            font-weight: {font_weight};
            font-size: 13px;
            cursor: pointer;
            transition: all 0.3s ease;
            transform: {transform};
            box-shadow: {shadow};
            font-family: 'Source Sans Pro', sans-serif;
            margin: 2px 4px;
            min-width: 80px;
            letter-spacing: 0.3px;
        "
        onmouseover="this.style.transform='scale(1.05)';this.style.boxShadow='0 4px 8px rgba(0,0,0,0.15)'"
        onmouseout="this.style.transform='{transform}';this.style.boxShadow='{shadow}'"
    >
        {texto}
    </button>
    '''
    return html

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Interfaz Principal
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

st.title("Control de Asistencia - Quinto Año")

# Selector de grupo
col1, col2 = st.columns([1, 4])

with col1:
    st.write("**Grupo:**")

with col2:
    grupo = st.radio(
        "Seleccionar Grupo",
        ["A", "B", "C"],
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
for idx, estudiante in enumerate(st.session_state.EstudiantesActuales):
    numero = estudiante["numero"]
    nombre = estudiante["nombre"]
    estado_actual = st.session_state.Asistencias[numero]
    
    with st.container():
        col1, col2, col3 = st.columns([0.5, 2.5, 7])
        
        with col1:
            st.write(f"**{numero}.**")
        
        with col2:
            st.write(f"**{nombre}**")
        
        with col3:
            # Crear los tres botones usando components
            html_presente = crear_boton_asistencia(
                "Presente", numero, st.session_state.GrupoSeleccionado, 
                estado_actual, "presente"
            )
            html_tardanza = crear_boton_asistencia(
                "Tardanza", numero, st.session_state.GrupoSeleccionado, 
                estado_actual, "tardanza"
            )
            html_ausente = crear_boton_asistencia(
                "Ausente", numero, st.session_state.GrupoSeleccionado, 
                estado_actual, "ausente"
            )
            
            # Mostrar los botones con components (mas confiable)
            st.components.v1.html(html_presente, height=45)
            st.components.v1.html(html_tardanza, height=45)
            st.components.v1.html(html_ausente, height=45)
        
        # Linea separadora
        if idx < len(st.session_state.EstudiantesActuales) - 1:
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
