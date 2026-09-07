import os
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
import requests

# Carga las variables del archivo .env si existe (entorno local)
load_dotenv()

API_KEY = os.getenv("IQAIR_API_KEY")
CIUDAD = "Monterrey"
ESTADO = "Nuevo Leon"
PAIS = "Mexico"


def obtener_datos_api():
    if not API_KEY:
        print("Error: No se ha configurado la IQAIR_API_KEY.")
        return None

    url = f"http://api.airvisual.com/v2/city?city={CIUDAD}&state={ESTADO}&country={PAIS}&key={API_KEY}"

    try:
        response = requests.get(url, timeout=15)
        datos = response.json()

        if datos.get("status") == "success":
            current = datos["data"]["current"]
            pollution = current["pollution"]

            ahora = datetime.now()
            return {
                "Fecha": ahora.strftime("%Y-%m-%d"),
                "Hora": ahora.strftime("%H:%M:%S"),
                "Ciudad": CIUDAD,
                "AQI_US": pollution["aqius"],
                "Contaminante_Principal": pollution["mainus"],
                "Temperatura_C": current["weather"]["tp"],
                "Humedad_%": current["weather"]["hu"],
            }
        else:
            print(f"Error en la API: {datos.get('data', {}).get('message')}")
            return None

    except Exception as e:
        print(f"Error en la consulta HTTP: {e}")
        return None


def guardar_en_csv(nuevo_registro):
    filepath = "data/calidad_aire.csv"
    os.makedirs("data", exist_ok=True)

    df_nuevo = pd.DataFrame([nuevo_registro])

    if os.path.exists(filepath):
        df_nuevo.to_csv(filepath, mode="a", header=False, index=False)
    else:
        df_nuevo.to_csv(filepath, mode="w", header=True, index=False)

    print(f"Registro guardado exitosamente en {filepath}")


if __name__ == "__main__":
    datos = obtener_datos_api()
    if datos:
        guardar_en_csv(datos)