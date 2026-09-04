import os
from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup


def extraer_datos_iqair():
    url = "https://www.iqair.com/mx/air-quality/mexico/nuevo-leon/monterrey"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error al acceder a la página: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    # Extraer AQI principal (AQI US)
    aqi_elem = soup.find("span", class_="aqi-value__value")
    aqi = aqi_elem.text.strip() if aqi_elem else "N/A"

    # Extraer Nivel de Contaminación (e.g., Moderado, Dañino)
    status_elem = soup.find("span", class_="aqi-status__text")
    estado = status_elem.text.strip() if status_elem else "N/A"

    # Extraer Contaminante Principal
    pollutant_elem = soup.find("p", class_="pollutant-item__name")
    contaminante_principal = (
        pollutant_elem.text.strip() if pollutant_elem else "N/A"
    )

    # Fecha y Hora actual
    ahora = datetime.now()
    fecha = ahora.strftime("%Y-%m-%d")
    hora = ahora.strftime("%H:%M:%S")

    return {
        "Fecha": fecha,
        "Hora": hora,
        "Ciudad": "Monterrey",
        "AQI_US": aqi,
        "Estado": estado,
        "Contaminante_Principal": contaminante_principal,
    }


def guardar_en_csv(nuevo_registro):
    filepath = "data/calidad_aire.csv"

    # Crear la carpeta data/ si no existe
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    df_nuevo = pd.DataFrame([nuevo_registro])

    # Si el archivo ya existe, añadir datos sin escribir el encabezado
    if os.path.exists(filepath):
        df_nuevo.to_csv(filepath, mode="a", header=False, index=False)
    else:
        df_nuevo.to_csv(filepath, mode="w", header=True, index=False)

    print("Registro agregado exitosamente.")


if __name__ == "__main__":
    datos = extraer_datos_iqair()
    if datos:
        guardar_en_csv(datos)