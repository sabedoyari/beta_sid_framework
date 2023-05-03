import urllib
import requests

DANE_GEOPORTAL_ENDPOINT = "https://geoportal.dane.gov.co/laboratorio/serviciosjson/buscador/searchAddress.php"

def dane_geocoding(address, code_department = '05', code_city = '001', rows_threshold = 20):

    """
    
    """
    
    dict_params = {
        'address' : address,
        'dpto': code_department,
        'mpio': code_city,
        'rows': rows_threshold
    }

    try:
        response = requests.get(
            url = DANE_GEOPORTAL_ENDPOINT,
            params = dict_params,
        )
        
        if len(response.json()['rows']) == 0:
            raise ValueError

        return response.json()['rows']
    
    except ValueError:
        print(f'Address: {address} not found.')

        return [
            {
                'D': address,
                'L': None,
                'G': None,
                'C': None,
                'P': None
            }
        ]
    
    except Exception as e:
        print(f'Process has failed, due {e}')
