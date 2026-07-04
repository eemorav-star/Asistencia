#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Universidad Tecnológica de Panamá 
# Semestral de Herramientas de programacion 1
# Integrantes: Jaen kathya, Luna Adrian, Mora Elpidio
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

import streamlit as st
import pandas as pd
from datetime import datetime
import openpyxl

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Lista con los nombres de los studiantes
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

Estudiantes = [ {"numero": 1, "nombre": "ALMANZA ABDUL"},
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
    {"numero": 15, "nombre": "HERMANDEZ MARISABEL"} ]

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Inicializar el estado de la sesion
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

if 'Asistencias' not in st.session_state:
    st.session_state.Asistencias = {}
    for estudiante in Estudiantes:
        st.session_state.Asistencias[estudiante["numero"]] = "Ausente"

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Titulo de la aplicacion asistencia
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

st.title("Control de Asistencia - Quinto Año A")

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Fecha y hora actual
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

now = datetime.now()
FechaHora = now.strftime("%d/%m/%Y %H:%M:%S")
st.write(f"**Fecha y Hora:** {FechaHora}")

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Registro de la asistencia
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

st.subheader("Registro de Asistencia")

for estudiante in Estudiantes:
    num = estudiante["numero"]
    nombre = estudiante["nombre"]
    
    col1, col2, col3, col4 = st.columns([1, 4, 1, 1])
    
    with col1:
        st.write(f"**{num}**")
    with col2:
        st.write(nombre)
    with col3:
        if st.button("Presente", key=f"Presente_{num}"):
            st.session_state.Asistencias[num] = "Presente"
            st.rerun()
    with col4:
        if st.button("Tardanza", key=f"Tardanza_{num}"):
            st.session_state.Asistencias[num] = "Tardanza"
            st.rerun()

st.divider()

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Resumen final de la asistencia
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

st.subheader("Resumen de Asistencia")

ContadorPresentes = 0
ContadorTardanzas = 0
ContadorAusentes = 0
i = 0

while i < len(Estudiantes):
    num = Estudiantes[i]["numero"]
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
# Botón para volver a reiniciar la asistencia
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

if st.button("Reiniciar Asistencia"):
    for estudiante in Estudiantes:
        st.session_state.Asistencias[estudiante["numero"]] = "Ausente"
    st.rerun()

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Lista detallada de asistencias
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

with st.expander("Ver lista completa de asistencias"):
    data = []
    for estudiante in Estudiantes:
        data.append({
            "Numero": estudiante["numero"],
            "Nombre": estudiante["nombre"],
            "Estado": st.session_state.Asistencias[estudiante["numero"]]
        })
    df = pd.DataFrame(data)
    st.dataframe(df)
