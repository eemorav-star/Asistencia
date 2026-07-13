#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# Universidad Tecnologica de Panama
# Semestral de Herramientas de Programacion 1
# Integrantes: Jaen Kathya, Luna Adrian, Mora Elpidio
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

from datetime import datetime

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# CONEXION A GOOGLE SHEETS
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

Scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]

Credenciales = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=Scopes
)

Cliente = gspread.authorize(Credenciales)

Libro = Cliente.open_by_key(
    "1L2akLixY8JG078yBpCDxezzVMsQo1XK7mzUlrwdM6Cs"
)

Hoja = Libro.worksheet("ASISTENCIA")

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# CONFIGURACION DE LOS GRUPOS
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

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

#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# FUNCION PARA GUARDAR LA ASISTENCIA
#ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

def GuardarAsistencia(Grupo, Estudiantes, Asistencias):

    FilaInicio = GRUPOS[Grupo]["fila_inicio"]
    FilaFin = GRUPOS[Grupo]["fila_fin"]
    FilaFecha = GRUPOS[Grupo]["fila_fecha"]

    Columna = None

    # Buscar la primera columna vacia entre C y M

    for C in range(3, 14):

        Vacia = True

        for Fila in range(FilaInicio, FilaFin + 1):

            Valor = Hoja.cell(Fila, C).value

            if Valor is not None and str(Valor).strip() != "":

                Vacia = False
                break

        if Vacia:

            Columna = C
            break

    if Columna is None:

        raise Exception(
            "Ya no quedan columnas disponibles (C hasta M)."
        )

    # Guardar fecha

    Hoja.update_cell(

        FilaFecha,

        Columna,

        datetime.now().strftime("%d/%m/%Y")

    )

    # Guardar asistencia

    Fila = FilaInicio

    for Estudiante in Estudiantes:

        Estado = Asistencias[Estudiante["numero"]]

        if Estado == "Presente":

            Hoja.update_cell(

                Fila,

                Columna,

                "."

            )

        elif Estado == "Tardanza":

            Hoja.update_cell(

                Fila,

                Columna,

                "T"

            )

        else:

            Hoja.update_cell(

                Fila,

                Columna,

                "---"

            )

        Fila += 1
