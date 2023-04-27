import pandas as pd
import numpy as np
import requests
from geopy.geocoders import Nominatim
import mysql.connector
import sys

sys.path.append('../')
from src import soporte_variables as spv



# EXTRACCCIÓN DE DATOS DE LA API
def extraccion_json(pais):
    """Esta función realiza la extracción de los datos de la API de "Universities Hipolabs". Realiza la extracción de los 
    datos en formato .json, mostrando tanto el código de estado como la razón del mismo. A continuación printea el nº de diccionarios incluidos en la lista resultado y sus keys.
    Parámetros:
        - pais (str): país del que queremos extraer los datos
    Return: lista de diccionarios con los datos (formato .json).
    """
    url = f'http://universities.hipolabs.com/search?country={pais.lower()}'
    resp = requests.get(url=url)
    print(f'Status code extracción {pais}: {resp.status_code}')
    print(f'Reason extracción {pais}: {resp.reason}')
    resp_json = resp.json()
    print(f'El resultado obtenido es una lista de diccionarios. Nº de elementos de la lista resultado: {len(resp_json)}')
    print(f'Las keys de cada diccionario son {len(resp_json[0])}: {resp_json[0].keys()}')
    return resp_json


def extraccion_api_df(pais, df_origen):
    """Esta función realiza la extracción de los datos de la API de "Universities Hipolabs". Realiza la extracción de los datos en formato .json, mostrando tanto el código
    de estado como la razón del mismo. A continuación printea el nº de diccionarios incluidos en la lista resultado y sus keys. Luego crea un dataframe con esos datos, printea 
    su número de filas y columnas y finalemnte concatena ese dataframe con el dataframe original introducido como argunmento.
    Parámetros:
        - pais (str): país del que queremos extraer los datos
        - df_origen (pandas.core.frame.DataFrame)
    Return: dataframe concatenando los datos del dataframe original que introducimos como argumento y los datos extraidos de la API para el país indicado.
    """
    url = f'http://universities.hipolabs.com/search?country={pais.lower()}'
    resp = requests.get(url=url)
    print(f'Status code extracción {pais}: {resp.status_code}')
    print(f'Reason extracción {pais}: {resp.reason}')
    resultado = resp.json()
    print(f'Nº de elementos de la lista resultado de {pais}: {len(resultado)}')
    print(f'Las keys de cada diccionario de {pais} son {len(resultado[0])}: {resultado[0].keys()}')
    df_pais = pd.DataFrame(resultado)
    print(f'Añadimos al dataframe resultado las {df_pais.shape[0]} filas y {df_pais.shape[1]} columnas de {pais}')
    df_origen = pd.concat([df_origen, df_pais], axis=0, ignore_index=True)
    return df_origen



# EDA
# Exploración numérica del dataframe
def explorar_df(dataframe, nombre = ''):
    """Esta función realiza la exploración inicial de un dataframe dado:
            - Muestra las 5 primeras filas
            - Muestra las 5 últimas filas
            - Muestra 10 filas aleatorias
            - Indica el nº de filas y columnas
            - Muestra el resultado del método .info()
            - Indica el número de nulos por columna en valor absoluto y porcentaje
            - Indica el nº de filas duplicadas. En caso de que no pueda realizar la comprobación muestra un error
            - Muestra los principales estadísticos tanto de las columnas numéricas (si las hay) como de las categóricas (si las hay)
            - Muestra el nombre de las columnas
            - Indica el numero de valores distintos de cada columna y muestra los valores cuando sean 15 o menos          
        Parámetros:
            - dataframe (pandas.core.frame.DataFrame): dataframe que se requiere explorar
            - nombre (str): nombre del dataframe a explorar. Parámetro por defecto con valor '' para que si n o se le quiere poner un nombre al dataframe
              la exploración pueda continuar.
        Return: None.
    """
    print(f'EXPLORACIÓN DEL DATAFRAME {nombre.upper()}')
    print('---------------------------------------------------------------------------')
    print(f'Las primeras 5 filas del dataframe {nombre} son:')
    display(dataframe.head())
    print('---------------------------------------------------------------------------')
    print(f'Las últimas 5 filas del dataframe {nombre} son:')
    display(dataframe.tail())
    print('---------------------------------------------------------------------------')
    print(f'A comntinuación se muestran 10 filas aleatorias del dataframe {nombre}:')
    display(dataframe.sample(10))
    print('---------------------------------------------------------------------------')
    print(f'El dataframe {nombre} tiene {dataframe.shape[0]} filas y {dataframe.shape[1]} columnas')
    print('---------------------------------------------------------------------------')
    print('A continuación el resultado del método .info() incluyendo los tipos de dato de cada columna:')
    dataframe.info()
    print('---------------------------------------------------------------------------')
    print('El número de nulos por columna en valor absoluto y porcentaje es:')
    for i, col in enumerate(dataframe.isnull().sum()):
        print(f'{dataframe.isnull().sum().index[i]}: nº de nulos: {col}. % de nulos: {round(col/dataframe.shape[0]*100, 2)} %')
    print('---------------------------------------------------------------------------')
    try:
        print(f'El nº de filas duplicadas del dataframe {nombre} es: {df.duplicated().sum()}')
    except:
        print(f'Ha ocurrido un error. No se ha podido comprobar si el dataframe {nombre} tiene filas duplicdas')
    print('---------------------------------------------------------------------------')
    if dataframe.select_dtypes(include=np.number).shape[1] != 0:
        print(f'Los principales estadísticos de las columnas numéricas son:')
        display(dataframe.describe().T)
    print('---------------------------------------------------------------------------')
    if dataframe.select_dtypes(exclude=np.number).shape[1] != 0:
        print(f'Los principales estadísticos de las columnas categóricas son:')
        display(dataframe.describe(include=object).T)
    print('---------------------------------------------------------------------------')
    print(f'El dataframe {nombre} tiene las siguientes columnas: \n{dataframe.columns}')
    print('---------------------------------------------------------------------------')
    print('El numero de valores distintos de cada columna es:')
    for col in dataframe.columns:
        if len(dataframe[col].value_counts()) > 15:
            print(f'{col}: {len(dataframe[col].value_counts())}')
        else:
            print(f'{col}: {len(dataframe[col].value_counts())}')
            print(f'Los valores únicos de la columna "{col}" son: {dataframe[col].unique()}')



# LIMPIEZA DEL DATAFRAME
def limpieza(df):
    """Esta función realiza la limpieza completa del dataframe con los datos de la API de "Universities Hipolabs" mientras printea mensajes indicando los pasos realizados correctamente:
            - Realiza la homogeneización de columnas reemplazando los '-' por '_' y eliminando los espacios que pudiera haber al inicio o el final
            - Ordena las columnas
            - Elimina la columna con información redundante 'domains'
            - Separa con .explode() los datos de la columna 'web_pages'
            - Resetea el índice
            - Indica el número de duplicados filtrando por la columna "name" y los elimina en caso de que los haya
            - Sustituye None por np.nan en la columna 'state_province'
            - Rreemplaza los np.nan de la columna 'state_province' por 'Unknown'
            - Homogeneiza los valores de la columna 'state_province'
            - Con una lista de los valores únicos de la columna 'state_province' (salvo 'Unknown') usa la API de geopy para obtener los datos de latitud y longitud para cada provincia e introduce 
              los resultados en un dataframe (printeando un mensaje de aviso si no puede obtener los datos de alguna provincia)
            - Une ambos dataframes (el original y el de la latitud y longitud de las provincias) e indica el número de filas y columnas del dataframe resultado, así como su indice para poder comprobar
              que es contínuo
        Parámetros:
            - df (pandas.core.frame.DataFrame): dataframe que se requiere explorar
        Return: Dataframe limpio y con los datos de latitud y longitud de geopy.
    """
    # realizamos la homogeneización de columnas. Además de reemplazar los '-' por '_' utilizamos un .strip() por si hubiera algún espacio al inicio o el final que no vieramos
    col_new = {col : col.strip().replace('-', '_') for col in df.columns} 
    df = df.rename(columns = col_new)
    # ordenamos las columnas 
    df = df.reindex(columns=[df.columns[3], df.columns[0], df.columns[4], df.columns[2], df.columns[1], df.columns[-1]]) 
    print('Columnas homogeneizadas y ordenadas correctamente')
    # eliminamos la columna con información duplicada
    df.drop(columns='domains', inplace=True)
    print('Columnas redundante "domains" eliminada.')
    # separamos con el método .explode()
    df = df.explode('web_pages')
    print(f'Se han separado los datos de la columna "web_pages". El nuevo dataframe tiene {df.shape[0]} filas y {df.shape[1]} columnas')
    # reseteamos el índice
    df.reset_index(drop=True, inplace=True) 
    print('Índice reseteado correctamente.')
    # chequeamos si hay duplicados
    print(f'Si filtramos por la columna "name" tenemos {df["name"].duplicated().sum()} duplicados')
    # borramos las filas duplicadas si las hay
    if df["name"].duplicated().sum() > 0:
        df.drop_duplicates(subset=['name'], inplace=True, ignore_index=True)
        print(f'Duplicados eliminados. El nuevo dataframe tiene {df.shape[0]} filas y {df.shape[1]} columnas')
    else:
        pass
    # utilizamos el método .fillna para sustituir None por np.nan
    df['state_province'].fillna(value=np.nan,  axis=None, inplace=True)
    # reemplazamos los NaN de la columna 'state_province' por 'Unknown'
    print(f'La columna "state_province" tiene un {round((df["state_province"].isnull().sum() / df.shape[0]) * 100, 2)} % de nulos. Procedemos a reemplazarlos por "Unknown".')
    df['state_province'].replace(np.nan, 'Unknown', inplace=True)
    # para reemplazar todos los valores de la columna 'state_province' a la vez utilizamos .replace() con un diccionario
    df['state_province'] = df['state_province'].replace(spv.sustituir_provincias)
    print('Valores de la columna "state_province" homogeneizados')
    # creamos la lista de las provincias con los valores únicos
    provincias = df['state_province'].unique().tolist()
    provincias.remove('Unknown') # eliminamos este elemento para no solicitar sus coordenadas
    # usando la API de geopy obtenemos los datos de latitud y longitud para cada elemento único dela columna 'state_province'
    df_geopy = pd.DataFrame(columns=['state_province', 'latitude', 'longitude'])
    for loc in provincias:
        try:
            geolocator = Nominatim(user_agent='Maitane') # inicializamos el geolocator
            location = geolocator.geocode(loc) # solicitamos la localización
            df_i = pd.DataFrame({'state_province': loc, 'latitude': location.latitude, 'longitude': location.longitude}, index=[0]) # obtenemos la latitud y longitud en un dataframe
            df_geopy = pd.concat([df_geopy, df_i], axis=0, ignore_index=True)
        except:
            print(f'La provincia {loc} no ha podido ser localizada')
    print('Latitud y longitud de las provincias obtenidas')
    # unimos ambos dataframes
    df = df.merge(df_geopy, how='left', on='state_province').reset_index(drop=True)
    print(f'Se han inluido la latitud y longitud en el dataframe original. El dataframe completo tiene {df.shape[0]} filas y {df.shape[1]} columnas')
    print(f'A continuación se muestra su indice para comprobar que es contínuo: {df.index}')
    return df



# CARGA EN SQL
# Creación de la base de datos
def crear_bbdd(datos_acceso, nombre_bbdd):
    """Esta función crea la base de datos de MySQL Workbench.
            - Printea un mensaje indicando que la conexión se ha realizado con éxito
            - Comprueba si la BBDD existe antes de crearla
            - Printea el cursor después de ejecutarlo como comprobación
            - Muestra un mensaje de error si la conexión falla indicando información de utilidad a cerca del error.
        Parámetros:
            - datos_acceso (dict): diccionario con los datos de acceso, formados por las keys 'user', 'password', 'host' y 'raise_on_warnings' (toma un bool como value)
            - nombre_bbdd (str): nombre que queremos darle al schema de la BBDD en MySQL Workbench.
        Return: None.
    """    
    mydb = mysql.connector.connect(**datos_acceso)
    print('Conexión realizada con éxito')
    mycursor = mydb.cursor()
    try:
        mycursor.execute(f'CREATE DATABASE IF NOT EXISTS {nombre_bbdd};')
        print(mycursor)
    except mysql.connector.Error as err:
        print(err)
        print('Error Code:', err.errno)
        print('SQLSTATE', err.sqlstate)
        print('Message', err.msg)

# creación de tablas e inserción de datos
def crear_insertar_tabla2(datos_acceso, query):
    """Esta función crea las tablas e inserta los datos en la base de datos de MySQL Workbench.
            - Printea un mensaje indicando que la conexión se ha realizado con éxito
            - Comprueba si la BBDD existe antes de crearla
            - Printea el cursor después de ejecutarlo como comprobación
            - Muestra un mensaje de error si la conexión falla indicando información de utilidad a cerca del error.
        Parámetros:
            - datos_acceso (dict): diccionario con los datos de acceso, formados por las keys 'user', 'password', 'host' y 'raise_on_warnings' (toma un bool como value)
            - query (str): query con el código de MySQL correspondiente a la tarea que se desea realizar (creación de tabla o inserción de valores)
        Return: None.
    """ 
    cnx = mysql.connector.connect(**datos_acceso)
    mycursor = cnx.cursor()
    try: 
        mycursor.execute(query)
        cnx.commit() 
    except mysql.connector.Error as err:
        print(err)
        print('Error Code:', err.errno)
        print('SQLSTATE', err.sqlstate)
        print('Message', err.msg)
