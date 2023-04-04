
import os
import base64
import json
import requests

import logging
import sys
import traceback
from functools import wraps
from typing import Callable



jira_api_token = "ATATT3xFfGF0VIQoWgA9lN3YkLcuM1nB3iGukoLk__Obxah89vKNx598-w-BRDb0E3_-UDQzYdti0coLm5-dw11SsxyIgNJAIxvfMGWi4pZhMAUKVxahZlq_fSNW0ONizEnrrTZvs1o4WwNK_ynrK8SIkyy3-4Rfm8iB5jorcs3szQMgdCw_IhE=681D9C3A"
jira_username = 1
jira_api_url = "https://itsham-sajid.atlassian.net/rest/api/3"

def create_logger() -> str:
    """Create Logger function to setups logger for this file."""
    # Logging variables
    logger_name = "ticket_feeder_logger"
    script_name_bare = os.path.splitext(sys.argv[0])[0].replace("./", "")
    logfile_name = script_name_bare + ".log"
    logging_filename = logfile_name
    logging_level = logging.INFO
    # Logging Configuration
    log_format = "[%(asctime)s] %(levelname) - 8s %(name) -12s %(message)s"
    logging.basicConfig(
        level=logging_level,
        format=log_format,
        handlers=[logging.StreamHandler(), logging.FileHandler(logging_filename)],
    )
    return logger_name


# Global logger
logger = logging.getLogger(create_logger())

def log_exception(func: Callable):
    """Logging declarator to ensure any exceptions seen are logged."""

    @wraps(func)
    def exception_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"There was a problem in {func.__name__}:\n{str(e)}")
            logger.error(traceback.format_exc())
            raise Exception(traceback.format_exc())

    return exception_wrapper


@log_exception
def get_api_auth_headers(username: str, api_token: str):
    """Create JIRA API basic auth headers with username and API token"""

    try:

        if not isinstance(username, str):
            raise TypeError("Username should be a string.")
        if not isinstance(api_token, str):
            raise TypeError("API token should be a string.")
        
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
    
    except TypeError as e:
        logger.error(str(e))
        return None

@log_exception
def api_connection_test(api_url, auth_headers) -> bool:

    """Test API connection with supplied creds"""

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
def connection_test():
    auth = get_api_auth_headers(jira_username, jira_api_token)
    # test = api_connection_test(jira_api_url, auth)

    return auth


print(connection_test())
