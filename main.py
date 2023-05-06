import json
import sys
import argparse
from scripts.infrastructure.potholes_person_notifications import *
from sid_framework.utils.geographic.address_geocoding import dane_geocoding

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
    # data = {'number': [573218769571, 573214942488],
    #         'nombre': ['Luis Felipe', 'Santiago'],
    #         'barrio': ['Jesús Nazareno', 'Calle Larga']}
    # df = pd.DataFrame(data)

    # Una vez potholes_person_notifications corra se podrá ejecutar con la df generada

    # Mensaje 1
    # send_message(df, 'huecos', 3609, 'prueba_local_7')

    # Mensaje 2
    # send_message(df, 'huecos_mensaje2', 3640, 'prueba_local_8')
