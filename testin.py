import os


def function():
    for var_name in ["JIRA_API_TOKEN", "JIRA_USERNAME", "JIRA_API_URL"]:
        if var_name not in os.environ:
            print(f"{var_name} environment variable is not set.")
            return False
    return True

function()