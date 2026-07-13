#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Universidad Tecnologica de Panama
# Semestral de Herramientas de Programacion 1
# Integrantes: Jaen Kathya, Luna Adrian, Mora Elpidio
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# --- Configuración de Google Sheets desde Secrets ---
def conectar_google_sheets():
    # Definir el alcance de la API
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    # Obtener las credenciales desde los secretos de Streamlit
    creds_dict = dict(st.secrets["gcp_service_account"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)

    # Autorizar al cliente de gspread
    client = gspread.authorize(creds)
    return client

# --- Configuración de grupos ---
GRUPOS = {
    "A": {
        "fila_inicio": 8,
        "fila_fin": 22,
        "fila_fecha": 7
    },
    "B": {
        "fila_inicio": 46,
        "fila_fin": 60,
        "fila_fecha": 45
    },
    "C": {
        "fila_inicio": 86,
        "fila_fin": 101,
        "fila_fecha": 85
    }
}

def GuardarAsistencia(grupo, estudiantes, asistencias):
    try:
        # 1. Conectar a Google Sheets
        client = conectar_google_sheets()

        # 2. Abrir el libro y la hoja
        libro = client.open("Libreta")
        hoja = libro.worksheet("ASISTENCIA")

        # 3. Obtener la configuración del grupo
        fila_inicio = GRUPOS[grupo]["fila_inicio"]
        fila_fin = GRUPOS[grupo]["fila_fin"]
        fila_fecha = GRUPOS[grupo]["fila_fecha"]

        # 4. Buscar la primera columna vacía entre C y M
        columna = None
        for c in range(3, 14):  # C=3, M=13
            columna_vacia = True
            rango_celdas = hoja.range(fila_inicio, c, fila_fin, c)
            for celda in rango_celdas:
                if celda.value is not None and celda.value != "":
                    columna_vacia = False
                    break
            if columna_vacia:
                columna = c
                break

        if columna is None:
            raise Exception("Ya no quedan columnas disponibles (C hasta M).")

        # 5. Escribir la fecha en el encabezado
        hoja.update_cell(fila_fecha, columna, datetime.now().strftime("%d/%m/%Y"))

        # 6. Escribir las asistencias
        fila = fila_inicio
        for estudiante in estudiantes:
            estado = asistencias[estudiante["numero"]]
            if estado == "Presente":
                valor = "."
            elif estado == "Tardanza":
                valor = "T"
            else:
                valor = "---"
            hoja.update_cell(fila, columna, valor)
            fila += 1

        st.success("Asistencia guardada exitosamente en Google Sheets")

    except Exception as e:
        st.error(f"❌ Error al guardar: {e}")
        raise
