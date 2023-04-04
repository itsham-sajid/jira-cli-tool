import base64
import json
import requests
from main import log_exception


@log_exception
def jira_api(username, api_token):

    try:

        auth_header = username + ":" + api_token
        auth_header_bytes = auth_header.encode('ascii')
        base64_bytes = base64.b64encode(auth_header_bytes)
        base64_auth_header = base64_bytes.decode('ascii')

        headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Basic " + base64_auth_header
        }
        
        return headers
    
    except Exception as e:
        print(f"\nERROR - An error occurred in __main__(): \n{e}")


@log_exception
def api_connection_test(api_url, auth_headers):

    response = requests.get(api_url + "/myself",  headers=auth_headers)
    
    if response.status_code == 200:
        response_data = response.json()
        response_email = response_data['emailAddress']
        logger.info(f"API Response Status Code: {response.status_code}")
        print(f"\nAuthenticated with user: {response_email}")
        return True
            
    logger.error(json.dumps(response.json(), indent=2))
    return False
        

@log_exception
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