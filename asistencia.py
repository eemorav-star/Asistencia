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

def aplicar_estilos():
    st.markdown("""
    <style>
        /* Estilo base para botones */
        .stButton button {
            border-radius: 20px !important;
            padding: 6px 18px !important;
            font-size: 13px !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            margin: 2px 4px !important;
            min-width: 80px !important;
            border: 2px solid #d1d5db !important;
            background-color: #f3f4f6 !important;
            color: #6b7280 !important;
            height: auto !important;
        }
        
        .stButton button:hover {
            transform: scale(1.05) !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
        }
        
        /* Estilo para boton Presente activo */
        .presente-activo {
            background-color: #1F77B4 !important;
            color: white !important;
            border-color: #1F77B4 !important;
            transform: scale(1.05) !important;
            box-shadow: 0 4px 12px rgba(31, 119, 180, 0.3) !important;
            font-weight: 700 !important;
        }
        
        /* Estilo para boton Tardanza activo */
        .tardanza-activo {
            background-color: #22C55E !important;
            color: white !important;
            border-color: #22C55E !important;
            transform: scale(1.05) !important;
            box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3) !important;
            font-weight: 700 !important;
        }
        
        /* Estilo para boton Ausente activo */
        .ausente-activo {
            background-color: #dc3545 !important;
            color: white !important;
            border-color: #dc3545 !important;
            transform: scale(1.05) !important;
            box-shadow: 0 4px 12px rgba(220, 53, 69, 0.3) !important;
            font-weight: 700 !important;
        }
        
        /* Contenedor de botones */
        div[data-testid="column"]:nth-child(3) {
            display: flex !important;
            flex-wrap: wrap !important;
            align-items: center !important;
            gap: 2px !important;
        }
        
        /* Mejorar tabla */
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
# Interfaz Principal
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

# Aplicar estilos
aplicar_estilos()

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
    
    col1, col2, col3 = st.columns([0.5, 2.5, 7])
    
    with col1:
        st.write(f"**{numero}.**")
    
    with col2:
        st.write(f"**{nombre}**")
    
    with col3:
        # Boton Presente
        boton_presente = st.button(
            "Presente", 
            key=f"P_{numero}_{grupo}_{idx}",
            use_container_width=False
        )
        if boton_presente:
            st.session_state.Asistencias[numero] = "Presente"
            st.rerun()
        
        # Aplicar clase CSS si esta activo
        if estado_actual == "Presente":
            st.markdown(f"""
            <script>
                (function() {{
                    const buttons = document.querySelectorAll('button');
                    for (let btn of buttons) {{
                        if (btn.textContent.trim() === 'Presente' && 
                            btn.id && btn.id.includes('P_{numero}_{grupo}_{idx}')) {{
                            btn.classList.add('presente-activo');
                        }}
                    }}
                }})();
            </script>
            """, unsafe_allow_html=True)
        
        # Boton Tardanza
        boton_tardanza = st.button(
            "Tardanza", 
            key=f"T_{numero}_{grupo}_{idx}",
            use_container_width=False
        )
        if boton_tardanza:
            st.session_state.Asistencias[numero] = "Tardanza"
            st.rerun()
        
        # Aplicar clase CSS si esta activo
        if estado_actual == "Tardanza":
            st.markdown(f"""
            <script>
                (function() {{
                    const buttons = document.querySelectorAll('button');
                    for (let btn of buttons) {{
                        if (btn.textContent.trim() === 'Tardanza' && 
                            btn.id && btn.id.includes('T_{numero}_{grupo}_{idx}')) {{
                            btn.classList.add('tardanza-activo');
                        }}
                    }}
                }})();
            </script>
            """, unsafe_allow_html=True)
        
        # Boton Ausente
        boton_ausente = st.button(
            "Ausente", 
            key=f"A_{numero}_{grupo}_{idx}",
            use_container_width=False
        )
        if boton_ausente:
            st.session_state.Asistencias[numero] = "Ausente"
            st.rerun()
        
        # Aplicar clase CSS si esta activo
        if estado_actual == "Ausente":
            st.markdown(f"""
            <script>
                (function() {{
                    const buttons = document.querySelectorAll('button');
                    for (let btn of buttons) {{
                        if (btn.textContent.trim() === 'Ausente' && 
                            btn.id && btn.id.includes('A_{numero}_{grupo}_{idx}')) {{
                            btn.classList.add('ausente-activo');
                        }}
                    }}
                }})();
            </script>
            """, unsafe_allow_html=True)
    
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
