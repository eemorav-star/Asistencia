#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Universidad Tecnologica de Panama 
# Semestral de Herramientas de programacion 1
# Integrantes: Jaen kathya, Luna Adrian, Mora Elpidio
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

import streamlit as st
import pandas as pd
from datetime import datetime
import openpyxl

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Datos de los estudiantes
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

estudiantes = [
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
    {"numero": 15, "nombre": "HERMANDEZ MARISABEL"}
]

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Inicializar el estado de la sesion
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

if 'asistencias' not in st.session_state:
    st.session_state.asistencias = {}
    for estudiante in estudiantes:
        st.session_state.asistencias[estudiante["numero"]] = "Ausente"

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Titulo y fecha/hora
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

st.title("Control de Asistencia - Quinto Año A")

now = datetime.now()
fecha_hora = now.strftime("%d/%m/%Y %H:%M:%S")
st.write(f"**Fecha y Hora:** {fecha_hora}")

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Registro de Asistencia
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

st.subheader("Registro de Asistencia")

for estudiante in estudiantes:
    num = estudiante["numero"]
    nombre = estudiante["nombre"]
    
    col1, col2, col3, col4 = st.columns([1, 4, 1, 1])
    
    with col1:
        st.write(f"**{num}**")
    with col2:
        st.write(nombre)
    with col3:
        if st.button("Presente", key=f"presente_{num}"):
            st.session_state.asistencias[num] = "Presente"
            st.rerun()
    with col4:
        if st.button("Tardanza", key=f"tardanza_{num}"):
            st.session_state.asistencias[num] = "Tardanza"
            st.rerun()

st.divider()

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Resumen de Asistencia
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

st.subheader("Resumen de Asistencia")

contador_presentes = 0
contador_tardanzas = 0
contador_ausentes = 0
i = 0

while i < len(estudiantes):
    num = estudiantes[i]["numero"]
    estado = st.session_state.asistencias[num]
    
    if estado == "Presente":
        contador_presentes += 1
    elif estado == "Tardanza":
        contador_tardanzas += 1
    else:
        contador_ausentes += 1
    i += 1

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Presentes", contador_presentes)
with col2:
    st.metric("Tardanzas", contador_tardanzas)
with col3:
    st.metric("Ausentes", contador_ausentes)

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Boton para reiniciar
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

if st.button("Reiniciar Asistencia"):
    for estudiante in estudiantes:
        st.session_state.asistencias[estudiante["numero"]] = "Ausente"
    st.rerun()