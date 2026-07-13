#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Universidad Tecnologica de Panama
# Semestral de Herramientas de Programacion 1
# Integrantes: Jaen Kathya, Luna Adrian, Mora Elpidio
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
#  Configuración de Google Sheets 
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
def conectar_google_sheets():
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    
    # Verificar que los secrets existen
    if "gcp_service_account" not in st.secrets:
        raise Exception(" No se encontró 'gcp_service_account' en Secrets")
    
    # Obtener credenciales
    creds_dict = dict(st.secrets["gcp_service_account"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    
    # Conectar
    client = gspread.authorize(creds)
    return client
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
#  Configuración de grupos 
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
GRUPOS = {
    "A": {"fila_inicio": 8, "fila_fin": 22, "fila_fecha": 7},
    "B": {"fila_inicio": 46, "fila_fin": 60, "fila_fecha": 45},
    "C": {"fila_inicio": 86, "fila_fin": 101, "fila_fecha": 85}}

def GuardarAsistencia(grupo, estudiantes, asistencias):
    try:
        # 1. Conectar a Google Sheets
        client = conectar_google_sheets()
        
        # 2. Abrir el libro y la hoja
        libro = client.open("Libreta")
        hoja = libro.worksheet("ASISTENCIA")
        
        # 3. Configuración del grupo
        fila_inicio = GRUPOS[grupo]["fila_inicio"]
        fila_fin = GRUPOS[grupo]["fila_fin"]
        fila_fecha = GRUPOS[grupo]["fila_fecha"]
        
        # 4. Buscar primera columna vacía (C=3 hasta M=13)
        columna = None
        for c in range(3, 14):
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
        
        # 5. Escribir fecha
        hoja.update_cell(fila_fecha, columna, datetime.now().strftime("%d/%m/%Y"))
        
        # 6. Escribir asistencias
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
        
        st.success(f" Asistencia guardada en Google Sheets (Columna {chr(64 + columna)})")
        return True
        
    except Exception as e:
        st.error(f"❌ Error al guardar: {str(e)}")
        return False
