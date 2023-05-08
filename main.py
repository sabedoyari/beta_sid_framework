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

    # df = potholes_person_notifications()

    # print(df.head())

    # Crear DataFrame de pruebas
    # data = {'number': [573218769571, 573214942488],
    #         'nombre': ['Luis Felipe', 'Santiago'],
    #         'barrio': ['Jesús Nazareno', 'Calle Larga']}
    # df = pd.DataFrame(data)

    df = pd.read_csv('data/processed_data/20230508_message1.csv')

    me = {'nombres': 'Luis',
          'celular': 573218769571,
          'nombre_barrio': 'Jesús Nazareno',
          'nombre_comuna': 'La Candelaria'}
    df = df.append(me, ignore_index=True)

    # print(df.head())

    # Una vez potholes_person_notifications corra se podrá ejecutar con la df generada

    # Mensaje 1
    send_message(df, 'huecos', 3609, '20230508_message1')

    # Mensaje 2
    # send_message(df, 'huecos_mensaje2', 3640, 'prueba_local_8')
