import streamlit as st
import pandas as pd

# Datos de los estudiantes
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

# Inicializar el estado de la sesión
if 'asistencias' not in st.session_state:
    st.session_state.asistencias = {}
    # Inicializar todos los estudiantes como "Ausente" por defecto
    for estudiante in estudiantes:
        st.session_state.asistencias[estudiante["numero"]] = "Ausente"

# Título de la aplicación
st.title("Control de Asistencia - Quinto Año A")

# Mostrar la lista de estudiantes con botones
st.subheader("Registro de Asistencia")

# Usar un bucle for para mostrar cada estudiante
for estudiante in estudiantes:
    num = estudiante["numero"]
    nombre = estudiante["nombre"]
    
    # Crear una fila para cada estudiante
    col1, col2, col3, col4 = st.columns([1, 4, 1, 1])
    
    with col1:
        st.write(f"**{num}**")
    with col2:
        st.write(nombre)
    with col3:
        if st.button("✅ Presente", key=f"presente_{num}"):
            st.session_state.asistencias[num] = "Presente"
            st.rerun()
    with col4:
        if st.button("⏰ Tardanza", key=f"tardanza_{num}"):
            st.session_state.asistencias[num] = "Tardanza"
            st.rerun()
    
    # Mostrar el estado actual
    estado = st.session_state.asistencias[num]
    if estado == "Presente":
        st.success(f"✅ {estado}")
    elif estado == "Tardanza":
        st.warning(f"⏰ {estado}")
    else:
        st.error(f"❌ {estado}")

# Separador visual
st.divider()

# Botón para calcular estadísticas
st.subheader("📊 Resumen de Asistencia")

# Usar un bucle while para contar las asistencias
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

# Mostrar los resultados en columnas
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("✅ Presentes", contador_presentes)
with col2:
    st.metric("⏰ Tardanzas", contador_tardanzas)
with col3:
    st.metric("❌ Ausentes", contador_ausentes)

# Botón para reiniciar la asistencia
if st.button("🔄 Reiniciar Asistencia"):
    for estudiante in estudiantes:
        st.session_state.asistencias[estudiante["numero"]] = "Ausente"
    st.rerun()

# Mostrar lista detallada (opcional)
with st.expander("📋 Ver lista completa de asistencias"):
    # Crear un DataFrame para mostrar los datos
    data = []
    for estudiante in estudiantes:
        data.append({
            "N°": estudiante["numero"],
            "Nombre": estudiante["nombre"],
            "Estado": st.session_state.asistencias[estudiante["numero"]]
        })
    df = pd.DataFrame(data)
    st.dataframe(df)