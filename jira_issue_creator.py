import base64
import json
import requests
from main import log_exception
import logging


logger = logging.getLogger(__name__)

@log_exception
def jira_api(username, api_token):

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

@log_exception
def api_connection_test(api_url, auth_headers):

    response = requests.get(api_url + "/myself",  headers=auth_headers)
    
    if response.status_code == 200:
        response_data = response.json()
        response_email = response_data['emailAddress']
        logger.info(f"- API Response Status Code: {response.status_code}")
        logger.info(f"- Authenticated with user: {response_email}")
        return True
            
    logger.error(json.dumps(response.json(), indent=2))
    return False
        

@log_exception
def send_payload(api_url, api_headers, data):

    ticket_counter = 0

    for item in data:
        issue = item
        
        response = requests.post(api_url + "/issue", headers=api_headers , data=json.dumps(issue))

        if response.status_code == 201:
            create_msg = response.text
            logger.info(f"- Ticket created: {create_msg}")
            ticket_counter += 1
        else:
            error_msg = response.text
            logger.error(f"- Failed to send payload: {response.status_code}")
            logger.error(f"- Error message: {error_msg}")
            
    logger.info(f"- Total tickets created: {ticket_counter}")        
    return response.status_code