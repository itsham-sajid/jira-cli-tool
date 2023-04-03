
import typer
import os
import rss_feed_search
import jira_issue_creator
import jira_template_format


app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})


@app.command(short_help="Command searches RSS feed with given search terms and outputs the results to a file")
def search_feed(
        rssfeed: str = typer.Option(..., "--rssfeed", "-r", help="The RSS feed URL", prompt=True),
        keywords: str = typer.Option(..., "--keywords", "-k", help="List of search terms", prompt=True),
        days: int = typer.Option(..., "--days", "-d", help="Number of days to search back", prompt=True)
        ):
    
    keywords = keywords.split(",")
    
    rss_feed_search.start_search_feed(keywords, rssfeed, days)


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

    check_files = jira_template_format.check_json_extension(jsondata, values)

    if check_files == True:
        print("YES")
        jira_format_task = jira_template_format.read_json_data_file(jsondata, templatefile, values, placeholders)
        jira_issue_creator.send_payload(jira_api_url, jira_api_auth, jira_format_task)
    else:
        print("NO")

    
@app.callback()
def main():
    """
    Feed2Ticket
    Purpose: This program allows you to create Jira tickets based on matching entries from an RSS feed.
    """

if __name__ == "__main__":

    try:

        """
        Program description.
        """
    

        jira_api_token = os.environ.get('JIRA_API_TOKEN')
        jira_username = os.environ.get('JIRA_USERNAME')
        jira_api_url = "https://itsham-sajid.atlassian.net/rest/api/3"

        jira_api_auth = jira_issue_creator.jira_api(jira_username, jira_api_token)
        jira_issue_creator.api_connection_test(jira_api_url, jira_api_auth)

        app()


    except Exception as e:
        print(f"\nERROR - An error occurred in __main__(): \n{e}")



 