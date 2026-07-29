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
# CSS para estilos de botones
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

def aplicar_estilos_botones():
    st.markdown("""
    <style>
        /* Estilo base para todos los botones */
        .stButton button {
            width: 100% !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
        }
        
        .stButton button:hover {
            transform: scale(1.05) !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
        }
        
        /* Botón Presente - estado normal (inactivo) */
        button[data-testid="baseButton-secondary"] {
            background-color: #e0e0e0 !important;
            color: #333333 !important;
            border: 2px solid #cccccc !important;
        }
        
        /* Botón Presente - estado activo (verde lima) */
        button[data-testid="baseButton-secondary"][data-estado="Presente"] {
            background-color: #A4DE02 !important;
            color: black !important;
            border: 2px solid #A4DE02 !important;
            transform: scale(1.05) !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
        }
        
        /* Botón Tardanza - estado activo (azul eléctrico) */
        button[data-testid="baseButton-secondary"][data-estado="Tardanza"] {
            background-color: #008CFF !important;
            color: white !important;
            border: 2px solid #008CFF !important;
            transform: scale(1.05) !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
        }
    </style>
    """, unsafe_allow_html=True)

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

# Aplicar estilos CSS
aplicar_estilos_botones()

# Crear contenedores para cada estudiante
for estudiante in st.session_state.EstudiantesActuales:
    numero = estudiante["numero"]
    nombre = estudiante["nombre"]
    estado_actual = st.session_state.Asistencias[numero]

    col1, col2, col3, col4 = st.columns([1,4,1,1])

    with col1:
        st.write(f"**{numero}**")

    with col2:
        st.write(nombre)

    with col3:
        # Botón Presente con atributo data-estado para CSS
        if st.button("Presente", key=f"P_{numero}_{grupo}"):
            st.session_state.Asistencias[numero] = "Presente"
            st.rerun()
        
        # Aplicar estilo según estado actual usando JavaScript
        if estado_actual == "Presente":
            st.markdown(f"""
            <script>
                (function() {{
                    const buttons = document.querySelectorAll('button');
                    for (let btn of buttons) {{
                        if (btn.textContent.trim() === 'Presente' && 
                            btn.id && btn.id.includes('P_{numero}_{grupo}')) {{
                            btn.style.backgroundColor = '#A4DE02';
                            btn.style.color = 'black';
                            btn.style.border = '2px solid #A4DE02';
                            btn.style.transform = 'scale(1.05)';
                            btn.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
                            btn.style.fontWeight = 'bold';
                        }}
                    }}
                }})();
            </script>
            """, unsafe_allow_html=True)

    with col4:
        # Botón Tardanza
        if st.button("Tardanza", key=f"T_{numero}_{grupo}"):
            st.session_state.Asistencias[numero] = "Tardanza"
            st.rerun()
        
        # Aplicar estilo según estado actual usando JavaScript
        if estado_actual == "Tardanza":
            st.markdown(f"""
            <script>
                (function() {{
                    const buttons = document.querySelectorAll('button');
                    for (let btn of buttons) {{
                        if (btn.textContent.trim() === 'Tardanza' && 
                            btn.id && btn.id.includes('T_{numero}_{grupo}')) {{
                            btn.style.backgroundColor = '#008CFF';
                            btn.style.color = 'white';
                            btn.style.border = '2px solid #008CFF';
                            btn.style.transform = 'scale(1.05)';
                            btn.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
                            btn.style.fontWeight = 'bold';
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
    st.metric("Presentes", ContadorPresentes, 
              delta=None, delta_color="normal")

with col2:
    st.metric("Tardanzas", ContadorTardanzas,
              delta=None, delta_color="normal")

with col3:
    st.metric("Ausentes", ContadorAusentes,
              delta=None, delta_color="normal")

st.divider()

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Botones de acción
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

col1, col2 = st.columns(2)

with col1:
    if st.button("Guardar Asistencia", key="guardar_asistencia"):
        try:
            GuardarAsistencia(
                st.session_state.GrupoSeleccionado,
                st.session_state.EstudiantesActuales,
                st.session_state.Asistencias
            )
            st.success("✅ La asistencia fue guardada correctamente.")
        except Exception as e:
            st.error(f"❌ Error al guardar: {e}")

with col2:
    if st.button("Reiniciar Asistencia", key="reiniciar_asistencia"):
        for estudiante in st.session_state.EstudiantesActuales:
            st.session_state.Asistencias[estudiante["numero"]] = "Ausente"
        st.success("🔄 Asistencia reiniciada.")
        st.rerun()

st.divider()

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Vista previa
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

VerVistaPrevia = st.checkbox("📊 Ver vista previa antes de descargar")

if VerVistaPrevia:
    FilasPreview = []
    for estudiante in st.session_state.EstudiantesActuales:
        num = estudiante["numero"]
        nombre = estudiante["nombre"]
        estado = st.session_state.Asistencias[num]
        FilasPreview.append({"N°": num, "Nombre": nombre, "Estado": estado})

    DfPreview = pd.DataFrame(FilasPreview)
    st.dataframe(DfPreview, hide_index=True, use_container_width=True)
    
    # Botón para descargar CSV
    csv = DfPreview.to_csv(index=False)
    st.download_button(
        label="📥 Descargar CSV",
        data=csv,
        file_name=f"asistencia_grupo_{st.session_state.GrupoSeleccionado}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
    )
