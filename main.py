
import typer
import jira_issue_creator
import jira_template_format
import logging
import os
import sys
import json
import traceback
from typing import Callable
import rss_feed_search
from functools import wraps



app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})

env_api_token = 'JIRA_API_TOKEN'
env_username = 'JIRA_USERNAME'
env_api_url = 'JIRA_API_URL'


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
@app.command(short_help="Command searches RSS feed with given search terms and outputs the results to a file")
def search_feed(
        rssfeed: str = typer.Option(..., "--rssfeed", "-r", help="The RSS feed URL", prompt=True),
        keywords: str = typer.Option(..., "--keywords", "-k", help="List of search terms", prompt=True),
        days: int = typer.Option(..., "--days", "-d", help="Number of days to search back", prompt=True)
        ):
    
    keywords = keywords.split(",")
    
    rss_feed_search.start_search_feed(keywords, rssfeed, days)


@log_exception
@app.command(short_help=
        'Command requires all positional arguements to search for rss feed, updates Jira template and creates ticket\n')
def create_tickets(
        jsondata: str = typer.Option(..., "--jsondata", "-j", help="JSON file", prompt=True),
        values: str = typer.Option(..., "--values", "-v", help="Values to use from JSON file", prompt=True),
        templatefile: str = typer.Option(..., "--templatefile", "-t", help="JIRA Template file", prompt=True),
        placeholders: str = typer.Option(..., "--placeholders", "-p", help="Number of days to search back", prompt=True)
        ):
    
    values = [v.strip() for v in values.split(",")]
    placeholders = placeholders.split(",")
    #ensure all the checks are completed 

    jira_api_vars = check_env_vars_exist(env_api_token, env_username, env_api_url)

    logger.info(f"Checking {jsondata} contains requested values: {values}")
    check_jsonfile_values = check_json(jsondata, values)

    logger.info(f"Checking {templatefile} contains specified placeholders: {placeholders}")
    check_template_values = check_json(jsondata, placeholders)
    
    

    # print(check_req_arguments)


    # if get_env_variables == True:
    #     api_connection = jira_connection(jira_username, jira_api_token)
        
    #     jira_issue_creator.jira_api()
 


    # check_files = jira_template_format.check_json_extension(jsondata, values)


    # if check_files == True:
    #     print("YES")
    #     jira_format_task = jira_template_format.read_json_data_file(jsondata, templatefile, values, placeholders)
    #     jira_issue_creator.send_payload(jira_api_url, jira_api_auth, jira_format_task)
    # else:
    #     print("NO")

@log_exception
def jira_connection(username, api_token):
        
        api_auth_headers = jira_issue_creator.jira_api(username, api_token)

        test_connection = jira_issue_creator.api_connection_test(jira_api_url, api_auth_headers)

        print(test_connection)


@log_exception
def check_env_vars_exist(*args: str) -> bool:
    for arg in args:
        if not os.environ.get(arg):
            logger.error(f"{arg} environment variable is not set.")
            return False
    return True



def check_json(jsondata, values):

    file_checks_passed = False

    with open(jsondata, "r") as f:
        data = json.load(f)

    if not jsondata.endswith('.json'):
        raise ValueError('Error: JSON file required')
    else:
        file_type = True
        for key, value in data.items():
            if not all(item in value for item in values):
                logger.error(f"Not all search values exist.\nPlease check JSON objects in '{jsondata}' to make sure values {values} exist")
                file_checks_passed = False
                break
        else:
            logger.info(f"All requested values {values} exist in '{jsondata}'")
            file_checks_passed = True

    return file_checks_passed



@app.callback()
def main():
    """
    Feed2Ticket
    Purpose: This program allows you to create Jira tickets based on matching entries from an RSS feed.
    """




if __name__ == "__main__":
    app()



 