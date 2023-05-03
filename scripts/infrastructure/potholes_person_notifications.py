import os
import sys
sys.path.append(os.getcwd())

import re
import pandas as pd
from sid_framework.utils.data_lake.extract_data import HiveFetchData

CONFIG_PATH = 'configfile.ini'
FLAG_EXTRACT_DATA = True

#  ===============================
#  Extracción de Datos de Personas
#  ===============================

fecth_data_obj = HiveFetchData(CONFIG_PATH)

if FLAG_EXTRACT_DATA:
    fecth_data_obj.connect_hive()
    people_data = fecth_data_obj.extract_raw_data(
        sql_script = fecth_data_obj.data_params['SQL_EXTRACT_PEOPLE']
    )

print(f'Shape: {people_data.shape}')

#  ===================
#  Preparación de Datos
#  ===================

#  Ajustar nombres de las columnas
#  -------------------------------
people_data.columns = [
    re.split(r'\.(.*)', item)[1] for item in people_data.columns
]

#  Dar formato numérico
#  --------------------
people_data[['longitud_metrica', 'latitud_metrica']] = people_data[
    ['longitud_metrica', 'latitud_metrica']
].apply(pd.to_numeric, errors = 'coerce')

fecth_data_obj.close_connection()