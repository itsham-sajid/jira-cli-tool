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


def create_logger() -> str:
    """Create Logger function to setups logger for this file."""
    # Logging variables
    logger_name = "ticket_feeder_logger"
    script_name_bare = os.path.splitext(sys.argv[0])[0].replace("./", "")
    logfile_name = script_name_bare + ".log"
    logging_filename = logfile_name
    logging_level = logging.INFO
    # Logging Configuration
    log_format = "[%(asctime)s] - %(levelname) - 8s %(name) - -12s %(message)s"
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
    
    env_vars = ['JIRA_API_TOKEN', 'JIRA_USERNAME', 'JIRA_API_URL']

    values = [v.strip() for v in values.split(",")]
    placeholders = placeholders.split(",")

    
    if (check_env_vars(env_vars)) == True:

        env_var_values = {var: os.environ.get(var) for var in env_vars}
        auth_headers = jira_issue_creator.jira_api(env_var_values['JIRA_USERNAME'], env_var_values['JIRA_API_TOKEN'])
        api_connect_test = jira_issue_creator.api_connection_test(env_var_values['JIRA_API_URL'], auth_headers)


    if api_connect_test == True:

        logger.info(f"- Checking {jsondata} contains requested values: {values}")
        check_jsonfile_values = check_json(jsondata, values)

        logger.info(f"- Checking {templatefile} contains specified placeholders: {placeholders}")
        check_template_values = template_json(templatefile, placeholders)


    if check_template_values and check_jsonfile_values == True:
        
        jira_format_task = jira_template_format.read_json_data_file(jsondata, templatefile, values, placeholders)
        jira_issue_creator.send_payload(env_var_values['JIRA_API_URL'], auth_headers, jira_format_task)

@log_exception
def check_env_vars(env_vars):

    env_passed = False

    for var in env_vars:
        if var not in os.environ:
            logger.error(f"- {var} not found in environment variables")
            logger.error(f"- Please check all required env variables exist")
            env_passed = False
            break
        else:
            logger.info(f"- {var} found in environment variables.")
            env_passed = True
    return env_passed

@log_exception
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
                logger.error(f"- Not all search values exist.\nPlease check {values} exist in '{jsondata}'")
                file_checks_passed = False
                break
        else:
            logger.info(f"- All requested values {values} exist in '{jsondata}'")
            file_checks_passed = True

    return file_checks_passed

@log_exception
def template_json(template_file, search_placeholders):
    file_checks_passed = False

    with open(template_file, "r") as f:
        data = json.load(f)

    if not template_file.endswith('.json'):
        raise ValueError('Error: JSON file required')
    else:
        file_type = True
        for key, value in data.items():
            if any(search_term in str(value) for search_term in search_placeholders):
                logger.info(f"Found placeholders: {search_placeholders} in JSON file '{template_file}'")
                file_checks_passed = True
                break
        else:
            logger.error(f"Not all placeholder values exist. Please check {search_placeholders} exist in '{template_file}'")
            file_checks_passed = False

    return file_checks_passed



@app.callback()
def main():
    """
    Feed2Ticket
    Purpose: This program allows you to create Jira tickets based on matching entries from an RSS feed.
    """



if __name__ == "__main__":
    app()



 