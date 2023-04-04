import base64
import json
import requests
from main import log_exception


def send_payload(api_url, api_headers, data):

    try:

        for item in data:
            issue = item
            
            response = requests.post(api_url + "/issue", headers=api_headers , data=json.dumps(issue))

            if response.status_code == 201:
                create_msg = response.text
                print("Ticket created: {}".format(create_msg))

            else:
                error_msg = response.text
                print("Failed to send payload: {}".format(response.status_code))
                print("Error message: {}".format(error_msg))
                
        return response.status_code

    except Exception as e:
        print(f"\nERROR - An error occurred in __main__(): \n{e}")