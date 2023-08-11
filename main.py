# Consultar pronostico de 5 dias cada 3 horas da un pronostico
# --> https://openweathermap.org/forecast5
"""
con el parametro cnt=20, se pueden limitar a menos valores
siempre empieza tomando el dia de hoy hacia adelante el pronostico.
asi que por lo menos siempre hay un pronostico con fecha actual
maximo es 8 por dia ,y como son supuestamente 5 dias , 40 es el maximo valor posible
puede traer 6 dias tomando el dia actual pocos valores y el ultimo dias con menos de 8
"""


import requests
import pandas as pd
import utils

BASE_URL = "https://api.openweathermap.org/data/2.5/forecast?units=metric&cnt=40&"


def armar_diccionario(response):

    lista = list()
    # Estas columnas se repiten para la misma ciudad
    ciudad_id = response["city"]["id"]
    ciudad = response["city"]["name"]
    lat = response["city"]["coord"]["lat"]
    long = response["city"]["coord"]["lon"]

    #  Recorro todos los pronosticos de una ciudad
    for pronostico in response["list"]:
        # ver forecast5.json como ejemplo
        dic = dict()
        dic["dt"] = pronostico["dt"]
        dic["id"] = ciudad_id
        dic["ciudad"] = ciudad
        dic["lat"] = lat
        dic["lon"] = long
        dic["temp"] = pronostico["main"]["temp"]
        dic["sensacion"] = pronostico["main"]["feels_like"]
        dic["temp_min"] = pronostico["main"]["temp_min"]
        dic["temp_max"] = pronostico["main"]["temp_max"]
        dic["presion"] = pronostico["main"]["pressure"]  # hPa
        dic["humedad"] = pronostico["main"]["humidity"]  # %
        lista.append(dic)
    return lista


def consultar_cinco_dias(coordenadas):
    """
    Recibe como parametro la lista de coordenadas
    Devuelve una lista para este ejemplo con 400 elementos.
    40 pronosticos por 10 ciudades
    """
    lista_pronosticos = list()
    pos = 1
    for coordenada in coordenadas:
        url = BASE_URL + f"{coordenada}&appid={utils.API}"
        response = requests.get(url)

        if response.status_code == 200:
            print(f"{pos} - Coordenas OK: {coordenada}")
            response_json = response.json()
            lista_ciudad = armar_diccionario(response_json)
        else:
            print(f"Error codigo {response.status_code}")
            print(f"NO existe ciudad para la coordenada {coordenada}")
        pos += 1
        lista_pronosticos.extend(lista_ciudad)
    return lista_pronosticos


def generar_df(lista_ciudades):
    """
    Genero el dataframe a partir de la lista de coordenadas
    """

    pronosticos = consultar_cinco_dias(lista_ciudades)

    # Obtengo un dataframe con todas los pronosticos de todas las ciudades
    df = pd.DataFrame(pronosticos) 

    # Agrego las columnas de hora y fecha
    df['fecha'] = pd.to_datetime(df['dt'], unit='s').dt.date
    df['hora'] = pd.to_datetime(pd.to_datetime(df['dt'], unit='s'), format="%H:%M:%S").dt.time
    return df


def generar_csv(df):
    """
    Genero el archivo csv a partir del dataframe
    el formato del csv es tiempodiario_20230711.csv 
    """
    dias = obtener_dias(df,"fecha") # obtengo los dias para poder armar los csv

    for dia in dias:
        dia_str = dia.strftime('%Y%m%d')
        file_csv = f"tiempodiario_{dia_str}.csv"
        df_fecha = df[df.fecha == dia]
        df_fecha.sort_values(by=["ciudad","hora"], inplace=False) 
        df_fecha.to_csv(file_csv, index=False, encoding='utf-8')


def obtener_dias(dataframe, grupo):
    df_grupo = dataframe.groupby(grupo)
    datetimes = [key for key, value in df_grupo]
    return datetimes


if __name__ == "__main__":
    #ciudades = utils.rcia  
    ciudades = utils.coordList
    dataframe = generar_df(ciudades)
    generar_csv(dataframe)