# Jira Ticket Feeder

## Purpose

The purpose of this tool is to automate the process of creating Jira tickets with data from an RSS Feed or JSON document.

The creation of tickets using the Jira API is straightforwad when creating a ticket using plain text, however for rich text features and to make it more readable tickets have to be created using the Atlassian Document Format (ADF).

The ADF format is simply just a JSON structured document. There's a template within 'templates' folder of an example.

To update values in your Jira temaplte file, you simply just have to add "placeholders" of where you want your values to go and these will be updated.


**The script allows you to do the following:** 

- **Search RSS Feeds:** Before creating a ticket you can search an RSS feed with specified search terms and see what results are returned and the values you can add to your ticket.
- **Jira Template:** There's a default template within the 'templates' folder. See [Usage](##Usage) for more info on the using templates
- **Create Tickets:** Tickets are created using the values from the RSS feed. The Jira temaplte is formatted and the values are added to where there's a corresponding "placeholder" value in the Jira Template. The completed template is sent via the Jira API.



## Prerequisites

- Jira API username and API Token
- Python 3 - Tool tested using Python 3.11.2 


## Usage

### Jira API Creds

To publish JIRA tickets first set environment variables below or add this to your local terminal profile e.g. (.bashrc, .zshrc file)


        export JIRA_API_TOKEN=<token>
   
        export JIRA_USERNAME=<jira-username>
        
        export JIRA_API_URL=<jira-api-url>


### Virtual Env & Requirements

Create and and activate Python virtual environment: 

    python -m venv <name>

    source <name>/bin/activate


Install the required packages:

    pip3 install -r requirements.txt


## Commands

The tool has two main commands **search-feed** and **create-ticket**

#### search-feed - Command searches for given RSS feed with supplied keywords and outputs all matches entries to a JSON file.  

**Required arguments:**

* --rssfeed  - The URL of the RSS feed
* --keywords - Keywords to search for, keywords are matched against the RSS feed entry titles
* --days     - How far back to check

**Example usage:**

        python3 main.py search-feed \
        --rssfeed="https://aws.amazon.com/about-aws/whats-new/recent/feed/?&rss" \
        --keywords="Direct Connect" \
        --days=30

**Output:**




**create-tickets**


main.py \
    create-tickets \
    --rssfeed="https://aws.amazon.com/about-aws/whats-new/recent/feed/?&rss" \
    --keywords=EKS \
    --days=7 \
    --values=title,link \
    --placeholders=titles-placeholder,link-placeholder




