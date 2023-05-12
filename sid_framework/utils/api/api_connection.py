import requests
import json


def send_message(df, name, template_id, contact_list_name, day, time):
    # Convertir DataFrame a JSON
    json_data = df.to_json(orient="records")

    reqUrl = "https://app.scala360.com/webhook/alcaldia-med/campaign/external/store"

    headersList = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "2O9Mc5l8bbivWCBZvz6y"
    }

    payload = json.dumps({
        "name": name,
        "active": 1,
        "template_id": template_id,
        "list_type": "list",
        "contact_list_id": None,
        "segment_id": None,
        "contact_list_name": contact_list_name,
        "type": "scheduled",
        "dates": {
            "days": None,
            "day": day,
            "time": time
        },
        "contacts": json.loads(json_data)
    })

    response = requests.request(
        "POST", reqUrl, data=payload,  headers=headersList)

    print(response.text)
