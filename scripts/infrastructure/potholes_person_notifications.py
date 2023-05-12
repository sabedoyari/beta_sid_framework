from sid_framework.utils.data_lake.extract_data import HiveFetchData
from sid_framework.utils.change_files.banned_people import concat_files_xlsx
from sid_framework.utils.change_files.write_excel import write_excel
from sid_framework.utils.geographic.clean_address import dane_clean_address
from sid_framework.utils.geographic.address_geocoding import *
from sid_framework.utils.geographic.distances_computing import *
import pandas as pd
import numpy as np
import re
import os
import sys
sys.path.append(os.getcwd())
pd.options.mode.chained_assignment = None  # default='warn'


def potholes_person_notifications():
    CONFIG_PATH = 'configfile.ini'
    FLAG_EXTRACT_DATA = False

    #  ===============================
    #  Extracción de Datos de Personas
    #  ===============================

    fecth_data_obj = HiveFetchData(CONFIG_PATH)

    if FLAG_EXTRACT_DATA:
        fecth_data_obj.connect_hive()
        people_data = fecth_data_obj.extract_raw_data(
            sql_script=fecth_data_obj.data_params['SQL_EXTRACT_PEOPLE']
        )
        nbhds_data = fecth_data_obj.extract_raw_data(
            sql_script=fecth_data_obj.data_params['SQL_EXTRACT_NBHDS']
        )

        print(f'Shape: {people_data.shape}')

        print(f'Shape: {nbhds_data.shape}')

        #  ===================
        #  Preparación de Datos
        #  ===================

        #  Ajustar nombres de las columnas
        #  -------------------------------
        people_data.columns = [
            re.split(r'\.(.*)', item)[1] for item in people_data.columns
        ]

        nbhds_data.columns = [
            re.split(r'\.(.*)', item)[1] for item in nbhds_data.columns
        ]

        #  Dar formato numérico
        #  --------------------
        people_data[['longitud_metrica', 'latitud_metrica']] = people_data[
            ['longitud_metrica', 'latitud_metrica']
        ].apply(pd.to_numeric, errors='coerce')

        fecth_data_obj.close_connection()

        people_data = people_data.loc[:, ~people_data.columns.isin(
            ['nombre_barrio', 'nombre_comua'])]

        nbhds_data = nbhds_data[['codbarrio', 'nombre', 'nombre_com']]

        nbhds_data.columns = ['cod_barrio', 'nombre_barrio', 'nombre_comuna']

        df1 = people_data.merge(nbhds_data, on='cod_barrio', how='left')

    else:
        # Ejecutar en caso de caída del lago
        df1 = pd.read_csv('data/raw_data/df1.csv', low_memory=False)

    # Cargar vetados

    vetados = concat_files_xlsx('data/banned/message1')

    vetados['documento'] = vetados['documento'].astype(str)

    df1 = df1[~df1.documento.isin(vetados.documento)]

    # Modifica el archivo intervenciones

    path = 'data/raw_data/intervenciones.xlsx'

    raw_df = pd.read_excel(path, sheet_name='programación')

    raw_df = raw_df.rename(columns={'dirección': 'direccion'})

    raw_df['id'] = range(1, len(raw_df) + 1)

    raw_df['id'] = raw_df['id'].astype(str)

    raw_df['accion'] = '11111111111'

    print('Looking for addresses...')

    df2 = gg_geocoding(raw_df)

    # df2 = pd.DataFrame(
    #     {'address': raw_df['dirección'].apply(dane_clean_address)})

    write_excel(path, 'direcciones', df2[['dir']])

    # df2 = df2['address'].apply(dane_geocoding)

    # df2 = pd.DataFrame(list(df2))

    # df2 = df2.rename(columns={"L": "latitud", "G": "longitud"})

    # df2.dropna(subset=['latitud'], inplace=True)

    # df2 = df2[['longitud', 'latitud']]

    # df2 = df2.apply(pd.to_numeric, errors='coerce')

    write_excel(path, 'coordenadas', df2[['latitud', 'longitud']])

    input('Press ENTER to continue...')

    df2 = pd.read_excel('data/raw_data/intervenciones.xlsx',
                        sheet_name='coordenadas')

    data = get_metric_coordinates(df2['latitud'], df2['longitud'])

    df2['latitud_metrica'] = data['metric_latitude']
    df2['longitud_metrica'] = data['metric_longitude']

    personas = df1[['latitud_metrica', 'longitud_metrica']]

    personas = df1[['latitud_metrica', 'longitud_metrica']]
    personas = personas.replace('', np.nan)
    ejecutados = df2[['latitud_metrica', 'longitud_metrica']]

    # Calcula las distancias entre cada punto de intervención y los demás puntos
    distances = euclidean_distances(ejecutados, personas)
    # Se fija una distancia mínima entre los puntos
    distancia = 50

    # Se añade la nueva categoría a las personas que se deben informar
    df = pd.DataFrame()

    for id_distance, distance in enumerate(distances):
        cond = (distance > 0) & (distance <= distancia)
        temp_df = df1.loc[cond]
        #temp = df2.loc[id_distance, ['nro_reporte']]
        #temp_df['nro_reporte'] = temp[0]
        df = pd.concat([df, temp_df], axis=0)

    df = df.reset_index()

    df['edad'] = df['edad'].apply(pd.to_numeric, errors='coerce')

    df['nro_reporte'] = ''

    res = df.query('edad >= 18')

    res = res.sort_values(['nro_reporte', 'celular', 'edad'], ascending=False).drop_duplicates(
        ['nro_reporte', 'celular'], keep='first')

    vetados = res[['nro_reporte', 'celular', 'documento']]

    fecha_impacto = (pd.Timestamp.today() +
                     pd.DateOffset(1))

    vetados['fecha_impacto'] = fecha_impacto.strftime('%Y-%m-%d')

    res = res[['nombres', 'celular', 'nombre_barrio', 'nombre_comuna']]

    res['celular'] = pd.to_numeric(res['celular'], downcast='integer')

    res['celular'] = '57' + res['celular'].astype(str)

    res = res.reset_index(drop=True)

    print(f'Number of persons to be notified: {len(res)}')

    df3 = pd.read_excel('data/raw_data/datos_prueba.xlsx', converters={'nombres': str,
                                                                       'celular': str,
                                                                       'nombre_barrio': str,
                                                                       'nombre_comuna': str})

    if len(res) > 0:
        i = np.random.randint(low=1, high=len(res), size=len(df3))

        df3[['nombre_barrio', 'nombre_comuna']] = res.loc[i, [
            'nombre_barrio', 'nombre_comuna']].reset_index(drop=True)

        res = pd.concat([res, df3], axis=0)

    res.to_csv('data/processed_data/' + fecha_impacto.strftime('%Y%m%d') +
               '_message1.csv', index=False, encoding='utf-8-sig')

    vetados.to_excel('data/banned/message1/' +
                     fecha_impacto.strftime('%Y%m%d') + '.xlsx', index=False)

    return res
