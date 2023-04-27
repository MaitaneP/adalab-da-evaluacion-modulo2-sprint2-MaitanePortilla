# DA-promoD-Mod2-sprint2-MaitanePortilla
Este repositorio incluye los ejercicios de Maitane Portilla de la cuarta evaluación (Módulo 2, Sprint 2) de la promo D del bootcamp de Data Analytics de Adalab.

La documentación se ha organizado en las siguientes carpetas:
- [**datos:**](https://github.com/Adalab/DA-promoD-Mod2-sprint2-MaitanePortilla/tree/main/datos) Recoge los .csv y .plk con los datos descargados y limpios.
- **notebook:** Se incluye el archivo:
    * [***evaluacion-mod-2-sprint-2.ipynb***](https://github.com/Adalab/DA-promoD-Mod2-sprint2-MaitanePortilla/blob/main/notebook/evaluacion-mod-2-sprint-2.ipynb): contiene los ejercicios de la evaluación.
- **sql:** Se incluyen los siguientes archivos:
    * [***ERR-diagram.png***](https://github.com/Adalab/DA-promoD-Mod2-sprint2-MaitanePortilla/blob/main/sql/ERR-diagram.png): diagrama de la BBDD en MySQL Workbench.
    * [***bd-universidades.sql***](https://github.com/Adalab/DA-promoD-Mod2-sprint2-MaitanePortilla/blob/main/sql/bd-universidades.sql): contiene el script para la creación de la BBDD.
- **src:** Incluye los siguientes archivos:
    * [***soporte_clases.py***](https://github.com/Adalab/DA-promoD-Mod2-sprint2-MaitanePortilla/blob/main/src/soporte_clases.py): contiene el .py usado para almacenar la clase.
    * [***soporte_funciones.py***](https://github.com/Adalab/DA-promoD-Mod2-sprint2-MaitanePortilla/blob/main/src/soporte_funciones.py): contiene el .py usado para almacenar funciones.
    * [***soporte_variables.py***](https://github.com/Adalab/DA-promoD-Mod2-sprint2-MaitanePortilla/blob/main/src/soporte_variables.py): contiene el .py usado para almacenar variables.


A continuación se incluye un listado de las librerías utilizadas e importaciones requeridas:
    import pandas as pd
    import numpy as np
    import requests
    from geopy.geocoders import Nominatim
    import mysql.connector
    import sys

    sys.path.append('../')
    from src import soporte_variables as spv
    from src import soporte_funciones as spf
    from src import soporte_clases as spc