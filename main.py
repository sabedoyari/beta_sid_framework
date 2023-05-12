import json
import sys
import argparse
from scripts.infrastructure.potholes_person_notifications import *
from sid_framework.utils.geographic.address_geocoding import dane_geocoding
from sid_framework.utils.api.api_connection import send_message

parser = argparse.ArgumentParser()
parser.add_argument("--job", help="Specific job to be executed")
parser.add_argument("--arguments", help="Arguments file to execute")

# args = parser.parse_args()

# print(args.arguments)
# input = json.loads(args.arguments)

if __name__ == '__main__':
    # if args.job == "geocoding":
    #     print(dane_geocoding(**input))

        df = potholes_person_notifications()

        print(df.head())

    # Crear DataFrame de pruebas
    #     data = {'number': [573218769571],  # , 573214942488
    #             'nombre': ['Luis Felipe'],  # , 'Santiago'
    #             'barrio': ['Jesús Nazareno']}  # , 'Calle Larga'
    #     df = pd.DataFrame(data)

#     df = pd.read_csv('data/processed_data/20230512_message1.csv')

#     me = {'nombres': 'Luis',
#           'celular': 573218769571,
#           'nombre_barrio': 'Jesús Nazareno',
#           'nombre_comuna': 'La Candelaria'}
#     df = df.append(me, ignore_index=True)

#     df = df.rename(columns={'nombres': 'nombre',
#                             'celular': 'number',
#                             'nombre_barrio': 'barrio'})

#     df = df.drop(columns=['nombre_comuna'])

#     print(len(df))

#     print(df.head())

    #     # Una vez potholes_person_notifications corra se podrá ejecutar con la df generada

    # Mensaje 1
#     send_message(df=df,
#                  name='huecos',
#                  template_id=3609,
#                  contact_list_name='20230512_message1',
#                  day='12-05-2023',
#                  time='12:00')

    # Mensaje 2
    # send_message(df=df,
    #             name='huecos_mensaje2',
    #             template_id=3640,
    #             contact_list_name='prueba_local_8',
    #             day='10-05-2023',
    #             time='22:00')
