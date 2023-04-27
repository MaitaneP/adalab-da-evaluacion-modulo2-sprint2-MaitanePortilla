import pandas as pd
import numpy as np
import requests
from geopy.geocoders import Nominatim
import mysql.connector
import sys

sys.path.append('../')
from src import soporte_variables as spv




class Carga_sql:
    
    def conectar_sql(self, nombre_bbdd, contraseña):
        self.nombre_bbdd = nombre_bbdd
        self.contraseña = contraseña
    

    def crear_bbdd(self, nombre_bbdd, contraseña):
        mydb = mysql.connector.connect(host='localhost',
                                        user='root',
                                        password=f'{self.contraseña}')
        print('Conexión realizada con éxito')
        mycursor = mydb.cursor()
        try:
            mycursor.execute(f'CREATE DATABASE IF NOT EXISTS {self.nombre_bbdd};')
            print(mycursor)
        except mysql.connector.Error as err:
            print(err)
            print('Error Code:', err.errno)
            print('SQLSTATE', err.sqlstate)
            print('Message', err.msg)
          
        
    def crear_insertar_tabla(self, query):
        self.query = query
        cnx = mysql.connector.connect(user='root', 
                                        password=f'{self.contraseña}',
                                        host='127.0.0.1',
                                        database=f'{self.nombre_bbdd}')
        mycursor = cnx.cursor()
        try: 
            mycursor.execute(query)
            cnx.commit() 
        except mysql.connector.Error as err:
            print(err)
            print('Error Code:', err.errno)
            print('SQLSTATE', err.sqlstate)
            print('Message', err.msg)
