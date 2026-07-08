#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Universidad Tecnologica de Panama 
# Semestral de Herramientas de programacion 1 , 2026
# Integrantes: Jaen Kathya, Luna Adrian, Mora Elpidio
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

import streamlit as st
import pandas as pd
from datetime import datetime
import openpyxl

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Datos de los estudiantes por grupo
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

GrupoA = [
    {"numero": 1, "nombre": "ALMANZA ABDUL"},
    {"numero": 2, "nombre": "ALVAEZ LINDA"},
    {"numero": 3, "nombre": "AMORES BETZY"},
    {"numero": 4, "nombre": "APARICIO KARLA"},
    {"numero": 5, "nombre": "APU CHARLEY"},
    {"numero": 6, "nombre": "CABALLERO ASHELY"},
    {"numero": 7, "nombre": "CARVAJAL JULIAN"},
    {"numero": 8, "nombre": "CIGARRISTA MILAGRO"},
    {"numero": 9, "nombre": "CONCEPCION MAYRA"},
    {"numero": 10, "nombre": "CUBILLA MELVIZ"},
    {"numero": 11, "nombre": "DE FRIAS ANGELO"},
    {"numero": 12, "nombre": "FRANCO GISELLE"},
    {"numero": 13, "nombre": "GONZALEZ JOSE"},
    {"numero": 14, "nombre": "HERNANDEZ VLADIMIR"},
    {"numero": 15, "nombre": "HERMANDEZ MARISABEL"}]

GrupoB = [
    {"numero": 1, "nombre": "ADAMES CHRISTIE"},
    {"numero": 2, "nombre": "ALONSO GISSETH"},
    {"numero": 3, "nombre": "BERNAL EDWARD"},
    {"numero": 4, "nombre": "BERROCAL MACIEL"},
    {"numero": 5, "nombre": "CAMARENA ZORAIDA"},
    {"numero": 6, "nombre": "CAMPOS PHILLIPS"},
    {"numero": 7, "nombre": "CARRASCO OLIVER"},
    {"numero": 8, "nombre": "CEDEÑO LEYDIE"},
    {"numero": 9, "nombre": "CHUNG KARLA"},
    {"numero": 10, "nombre": "ESPINOSA MILEYKA"},
    {"numero": 11, "nombre": "FARRUGIA STEPAHANY"},
    {"numero": 12, "nombre": "FRANCO PEDRO"},
    {"numero": 13, "nombre": "GOMEZ ROSA"},
    {"numero": 14, "nombre": "GOMEZ PAOLO"},
    {"numero": 15, "nombre": "GRAJALES JULIO"}]

GrupoC = [
    {"numero": 1, "nombre": "ABREGO IVELIN"},
    {"numero": 2, "nombre": "AGAMES MELANY"},
    {"numero": 3, "nombre": "BECERRA LIZETH"},
    {"numero": 4, "nombre": "BERROCAL MARIEL"},
    {"numero": 5, "nombre": "CALDERON MERYLIN"},
    {"numero": 6, "nombre": "CANO JOSEPH"},
    {"numero": 7, "nombre": "CARDENAS JAIME"},
    {"numero": 8, "nombre": "CASTILLO MARIBEL"},
    {"numero": 9, "nombre": "DE LA ROSA GRETTELL"},
    {"numero": 10, "nombre": "DIAZ XAVIER"},
    {"numero": 11, "nombre": "DIAZ DANITZA"},
    {"numero": 12, "nombre": "DUARTE LUIS"},
    {"numero": 13, "nombre": "ESQUIVEL ADAN"},
    {"numero": 14, "nombre": "GARCIA JAIRO"},
    {"numero": 15, "nombre": "GRIFFITH SANDIVEL"},
    {"numero": 16, "nombre": "IBARRA JOSE"}]

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Diccionario para mapear grupos
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

Grupos = {"A": GrupoA,"B": GrupoB,"C": GrupoC}

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Inicializar estado de la sesion
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

if 'GrupoSeleccionado' not in st.session_state:
    st.session_state.GrupoSeleccionado = "A"

if 'EstudiantesActuales' not in st.session_state:
    st.session_state.EstudiantesActuales = GrupoA

if 'Asistencias' not in st.session_state:
    st.session_state.Asistencias = {}
    for estudiante in GrupoA:
        st.session_state.Asistencias[estudiante["numero"]] = "Ausente"

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Funcion para cambiar de grupo
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

def CambiarGrupo(grupo):
    st.session_state.EstudiantesActuales = Grupos[grupo]
    
    # Reiniciar asistencias para el nuevo grupo
    st.session_state.Asistencias = {}
    for estudiante in st.session_state.EstudiantesActuales:
        st.session_state.Asistencias[estudiante["numero"]] = "Ausente"
    
    st.session_state.GrupoSeleccionado = grupo
    st.rerun()

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Selector de grupo
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

st.title("Control de Asistencia - Quinto Año")

col1, col2 = st.columns([1, 3])
with col1:
    st.write("**Seleccionar Grupo:**")
with col2:
    grupo = st.radio("Selecciona el grupo", ["A", "B", "C"],
        index=0 if st.session_state.GrupoSeleccionado == "A" else 1 if st.session_state.GrupoSeleccionado == "B" else 2,
        horizontal=True,key="SelectorGrupo")

# Verificar si se cambio el grupo
if grupo != st.session_state.GrupoSeleccionado:
    CambiarGrupo(grupo)

st.write(f"**Grupo {st.session_state.GrupoSeleccionado} - {len(st.session_state.EstudiantesActuales)} estudiantes**")

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Fecha y hora
#oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

now = datetime.now()
FechaHora = now.strftime("%d/%m/%Y %H:%M:%S")
st.write(f"**Fecha y Hora:** {FechaHora}")

st.divider()

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Registro de Asistencia
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

st.subheader("Registro de Asistencia")

for estudiante in st.session_state.EstudiantesActuales:
    num = estudiante["numero"]
    nombre = estudiante["nombre"]
    
    col1, col2, col3, col4 = st.columns([1, 4, 1, 1])
    
    with col1:
        st.write(f"**{num}**")
    with col2:
        st.write(nombre)
    with col3:
        if st.button("Presente", key=f"Presente_{num}_{st.session_state.GrupoSeleccionado}"):
            st.session_state.Asistencias[num] = "Presente"
            st.rerun()
    with col4:
        if st.button("Tardanza", key=f"Tardanza_{num}_{st.session_state.GrupoSeleccionado}"):
            st.session_state.Asistencias[num] = "Tardanza"
            st.rerun()

st.divider()

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Resumen de la Asistencia
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

st.subheader("Resumen de Asistencia")

ContadorPresentes = 0
ContadorTardanzas = 0
ContadorAusentes = 0
i = 0

while i < len(st.session_state.EstudiantesActuales):
    num = st.session_state.EstudiantesActuales[i]["numero"]
    estado = st.session_state.Asistencias[num]
    
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

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Boton para reiniciar
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

if st.button("Reiniciar Asistencia"):
    for estudiante in st.session_state.EstudiantesActuales:
        st.session_state.Asistencias[estudiante["numero"]] = "Ausente"
    st.rerun()
