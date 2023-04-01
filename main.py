
import typer
import os
import json
import rss_feed_search
import jira_issue_creator
import jira_template_format


app = typer.Typer()



@app.command(short_help='Command requires all positional arguements to search for rss feed, updates Jira template and creates ticket')
def create_tickets(
        rssfeed: str = typer.Option(..., "--rssfeed", "-r", help="The RSS feed URL", prompt=True),
        keywords: str = typer.Option(..., "--keywords", "-k", help="List of search terms", prompt=True),
        days: int = typer.Option(..., "--days", "-d", help="Number of days to search back", prompt=True),
        values: str = typer.Option(..., "--values", "-v", help="Number of days to search back", prompt=True),
        placeholders: str = typer.Option(..., "--placeholders", "-p", help="Number of days to search back", prompt=True)
        ):
    
    
    keywords = keywords.split(",")

    get_rssfeed_data = rss_feed_search.start_search_feed(keywords, rssfeed, days)

    templatefile = "eks_release_template.json"

    requested_entries = {}


    values = [v.strip() for v in values.split(",")]

    for entry_num, entry in get_rssfeed_data.items():
        requested_entries[entry_num] = {}
        for value in values:
            if value in entry:
                requested_entries[entry_num][value] = entry[value]
            else:
                print(f"No value found for {value}")
    
    placeholders = placeholders.split(",")

    jira_format_task = jira_template_format.update_dict(requested_entries, placeholders, templatefile)

    # jira_issue_creator.send_payload(jira_api_url, jira_api_auth, jira_format_task)



@app.command(short_help="Command searches RSS feed with given search terms and outputs the results to a file")
def search_feed():
    print("Hello")



if __name__ == "__main__":

    try:

        jira_api_token = os.environ.get('JIRA_API_TOKEN')
        jira_username = os.environ.get('JIRA_USERNAME')
        jira_api_url = "https://itsham-sajid.atlassian.net/rest/api/3"

        jira_api_auth = jira_issue_creator.jira_api(jira_username, jira_api_token)
        jira_issue_creator.api_connection_test(jira_api_url, jira_api_auth)

        app()


    except Exception as e:
        print(f"\nERROR - An error occurred in __main__(): \n{e}")



 