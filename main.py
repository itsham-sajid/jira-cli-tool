import jira_issue_creator
import jira_template_format
import json
from logs import logger, log_exception
import os
import rss_feed_search
import typer

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})

@log_exception
@app.command(short_help="Command searches RSS feed with given search terms and outputs the results to a file")
def search_feed(
        rssfeed: str = typer.Option(..., "--rssfeed", "-r", help="The RSS feed URL", prompt=True),
        keywords: str = typer.Option(..., "--keywords", "-k", help="List of search terms", prompt=True),
        days: int = typer.Option(..., "--days", "-d", help="Number of days to search back", prompt=True)
        ):
    """ search-feed command:
     
    Command searches for given RSS feed and outputs all matches entries to a file.  

    """
    
    keywords = keywords.split(",")
    
    rss_feed_search.start_search_feed(keywords, rssfeed, days)

@log_exception
@app.command(short_help=
        'Command requires all positional arguements to provide JSON data, update Jira template and create tickets\n')
def create_tickets(
        jsondata: str = typer.Option(..., "--jsondata", "-j", help="JSON file", prompt=True),
        values: str = typer.Option(..., "--values", "-v", help="Values to use from JSON file", prompt=True),
        templatefile: str = typer.Option(..., "--templatefile", "-t", help="JIRA Template file", prompt=True),
        placeholders: str = typer.Option(..., "--placeholders", "-p", help="Number of days to search back", prompt=True)
        ):
    """ create-commands command:
     
    Command checks env vars exist, tests creds, checks values provided, updates Jira template and creates the Jira tickets  

    """
    
    logger.info("-" * 50)
    env_vars = ['JIRA_API_TOKEN', 'JIRA_USERNAME', 'JIRA_API_URL']

    values = [v.strip() for v in values.split(",")]
    placeholders = placeholders.split(",")

    
    if (check_env_vars(env_vars)) == True:

        env_var_values = {var: os.environ.get(var) for var in env_vars}
        auth_headers = jira_issue_creator.jira_api(env_var_values['JIRA_USERNAME'], env_var_values['JIRA_API_TOKEN'])
        logger.info("-" * 50)
        api_connect_test = jira_issue_creator.api_connection_test(env_var_values['JIRA_API_URL'], auth_headers)
        logger.info("-" * 50)

    if api_connect_test:
        logger.info(f"- Checking '{jsondata}' contains requested values: {values}")
        check_jsonfile_values = check_json(jsondata, values)

        if check_jsonfile_values:
            logger.info(f"- Checking '{templatefile}' contains specified placeholders: {placeholders}")
            check_template_values = template_checks(templatefile, placeholders)
        else:
            check_template_values = False
    else:
        check_jsonfile_values = False
        check_template_values = False

    if check_template_values and check_jsonfile_values:

        jira_format_task = jira_template_format.read_json_data_file(jsondata, templatefile, values, placeholders)
        logger.info("-" * 50)
        jira_issue_creator.send_payload(env_var_values['JIRA_API_URL'], auth_headers, jira_format_task)
        logger.info("-" * 50)

@log_exception
def check_env_vars(env_vars):
    """ Function checks required env vars exist. """

    env_passed = False

    for var in env_vars:
        if var not in os.environ:
            logger.error(f"- {var} not found in environment variables")
            logger.error(f"- Please check all required env variables exist")
            env_passed = False
            break
        else:
            logger.info(f"- {var} Found in environment variables.")
            env_passed = True
    return env_passed

@log_exception
def check_json(jsondata, values):
    """ Function performs checks against provide JSON files and if values exist within the file. """

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
def template_checks(template_file, search_placeholders):
    """ Function performs checks against Jira template file and checks placeholders values exist within the file. """

    file_checks_passed = False

    with open(template_file, "r") as f:
        data = json.load(f)

    if not template_file.endswith('.json'):
        raise ValueError('Error: JSON file required')
    else:
        file_type = True
        for key, value in data.items():
            if any(search_term in str(value) for search_term in search_placeholders):
                logger.info(f"- Found placeholders: {search_placeholders} in JSON file '{template_file}'")
                file_checks_passed = True
                break
        else:
            logger.error(f"- Not all placeholder values exist. Please check {search_placeholders} exist in '{template_file}'")
            file_checks_passed = False

    return file_checks_passed


@app.callback()
def main():
    """
    TicketFeeder
    Purpose: This program allows you to search for entries in a RSS Feed, the matching entries are saved to a JSON file.
    The saved JSON file can be used to create Jira tickets with the 'create-tickets' command.

    For full usage instructions please check README.md
    """

if __name__ == "__main__":
    app()



 