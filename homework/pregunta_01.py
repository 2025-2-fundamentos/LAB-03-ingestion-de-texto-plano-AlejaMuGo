"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel
import pandas as pd
import re

def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
    with open("files/input/clusters_report.txt", "r", encoding="utf-8") as f:
        lineas = f.readlines()

    # Saltamos encabezados (las 4 primeras líneas)
    lineas = lineas[4:]

    clusters = []
    cantidades = []
    porcentajes = []
    palabras_clave = []

    cluster_actual = None
    cantidad_actual = None
    porcentaje_actual = None
    partes_palabras = []

    patron_inicio = re.compile(r"\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s*(.*)")

    for linea in lineas:
        if linea.strip() == "":
            if cluster_actual is not None:
                texto = " ".join(partes_palabras)
                texto = " ".join(texto.split())
                if texto.endswith("."):
                    texto = texto[:-1]
                partes = [p.strip() for p in texto.split(",")]
                texto = ", ".join(partes)

                clusters.append(cluster_actual)
                cantidades.append(cantidad_actual)
                porcentajes.append(porcentaje_actual)
                palabras_clave.append(texto)

                cluster_actual = None
                partes_palabras = []
            continue

        m = patron_inicio.match(linea)
        if m:
            cluster_actual = int(m.group(1))
            cantidad_actual = int(m.group(2))
            porc_str = m.group(3).replace(",", ".")
            porcentaje_actual = float(porc_str)
            texto_palabras = m.group(4).strip()
            partes_palabras = [texto_palabras] if texto_palabras else []
        else:
            partes_palabras.append(linea.strip())

    if cluster_actual is not None:
        texto = " ".join(partes_palabras)
        texto = " ".join(texto.split())
        if texto.endswith("."):
            texto = texto[:-1]
        partes = [p.strip() for p in texto.split(",")]
        texto = ", ".join(partes)

        clusters.append(cluster_actual)
        cantidades.append(cantidad_actual)
        porcentajes.append(porcentaje_actual)
        palabras_clave.append(texto)

    df = pd.DataFrame(
        {
            "cluster": clusters,
            "cantidad_de_palabras_clave": cantidades,
            "porcentaje_de_palabras_clave": porcentajes,
            "principales_palabras_clave": palabras_clave,
        }
    )

    return df