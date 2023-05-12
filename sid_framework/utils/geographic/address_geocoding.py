import requests
import json
import pandas as pd

DANE_GEOPORTAL_ENDPOINT = "https://geoportal.dane.gov.co/laboratorio/serviciosjson/buscador/searchAddress.php"


def dane_geocoding(address, code_department='05', code_city='001', rows_threshold=20):
    """

    """

    dict_params = {
        'address': address,
        'dpto': code_department,
        'mpio': code_city,
        'rows': rows_threshold
    }

    try:
        response = requests.get(
            url=DANE_GEOPORTAL_ENDPOINT,
            params=dict_params,
        )

        if len(response.json()['rows']) == 0:
            raise ValueError

        return response.json()['rows'][0]

    except ValueError:
        print(f'Address: {address} not found.')

        return {
            'D': address,
            'L': None,
            'G': None,
            'C': None,
            'P': None
        }

    except Exception as e:
        print(f'Process has failed, due {e}')


def gg_geocoding(df):
    json_data = df.to_json(orient="records")

    url = "http://10.1.220.242/consultaPEEApi/consulta/jsonDir"

    parsed = json.loads(json_data)

    payload = json.dumps(parsed, indent=2)

    headers = {
        'user': 'datos',
        'pass': 'hfy7846*47',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    response = json.loads(response.text)
    response = pd.json_normalize(response)
    response = response[['dir', 'latitud', 'longitud']]

    response.to_csv('data/lats_and_lons.csv', index=False)

    return response
