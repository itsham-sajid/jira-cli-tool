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

#### search-feed
The command searches for given RSS feed with supplied keywords and outputs all matches entries to a JSON file.  

**Required arguments:**

* --rssfeed  - The URL of the RSS feed
* --keywords - Keywords to search for, keywords are matched against the RSS feed entry titles
* --days     - How far back to check

**Example usage:**

        python3 main.py search-feed \
        --rssfeed="https://aws.amazon.com/about-aws/whats-new/recent/feed/?&rss" \
        --keywords="Direct Connect" \ #multiple keyowrds can be declared with spaces e.g. --keywords=AWS,EKS
        --days=30

**Output: Saved to a file named '2-CodeBuild-entries.json'

        {
            "Entry 1": {
                "id": "1",
                "published": "Tue, 04 Apr 2023 21:48:5",
                "title": "AWS CodeBuild is now available in three additional AWS Regions",
                "link": "https://aws.amazon.com/about-aws/whats-new/2023/04/aws-codebuild-three-additional-regions/"
            },
            "Entry 2": {
                "id": "2",
                "published": "Tue, 28 Mar 2023 19:07:3",
                "title": "AWS CodeBuild supports Arm-based workloads in five additional AWS Regions",
                "link": "https://aws.amazon.com/about-aws/whats-new/2023/03/aws-codebuild-arm-based-workloads-additional-regions/"
            }
        }



#### create-tickets

How this commands works is it will first take your JSDON data file, you declare all the values you want to obtain your JSON file for your Jira ticket, provide your Jira template file which has 'placeholders' to where you want your values to be placed.

The command will format the Jira ADF template replacing all values and a seperate Jira ticket is raised for each entry in your JSON file. So, for the '2-CodeBuild-entries.json' file 2 tickets will be created.

The reason for using the Jira ADF template is because it's the only format their API accepts for rich text features. Hence, the reason for adding 'placeholders' and pulling values from your JSON data file their replaced with

**Required arguments:**

* --jsondata  - A JSON file with data for your ticket. Note: Seperate tickets are created for each item in your JSON file.
* --values - Declare values from the JSON file, this is being used to match with the 'placeholders' in the 'templatefile'
* --templatefile - The Jira ADF template file, sample template within 'templates/eks_release_template.json'
* --placeholders - Declare the 'placeholders'. This is where the 'values' your from 'jsondata' will go

**Example:** 

        python3 main.py create-tickets \
        --jsondata=2-CodeBuild-entries.json \
        --values=title,link" \ #multiple keyowrds can be declared with spaces e.g.
        --templatefile=eks_release_template.json \
        --placeholders=entries-placeholder,link-placeholder

**Output:**

From the above example, below is the expected result. 
**Two tickets are created within Jira:**
![image](https://user-images.githubusercontent.com/99727892/229946288-0eb1e161-1992-4316-832d-37c11c85005e.png)


**Task Details:**
![image](https://user-images.githubusercontent.com/99727892/229946579-3581eaac-18a3-43d7-ab5a-4d85d3b48c4f.png)
                                                                                                                                        
## Logging

The logging module contains the 

Below is the logging output for the creation of a ticket if all required arguments are met and have passed:

        [2023-04-05 00:43:19,701] - INFO     ticket_feeder_logger --------------------------------------------------
        [2023-04-05 00:43:19,701] - INFO     ticket_feeder_logger - JIRA_API_TOKEN Found in environment variables.
        [2023-04-05 00:43:19,701] - INFO     ticket_feeder_logger - JIRA_USERNAME Found in environment variables.
        [2023-04-05 00:43:19,715] - INFO     ticket_feeder_logger - JIRA_API_URL Found in environment variables.
        [2023-04-05 00:43:19,715] - INFO     ticket_feeder_logger --------------------------------------------------
        [2023-04-05 00:43:19,933] - INFO     jira_issue_creator - API Response Status Code: 200
        [2023-04-05 00:43:19,933] - INFO     jira_issue_creator - Authenticated with user: itshams@googlemail.com
        [2023-04-05 00:43:19,933] - INFO     ticket_feeder_logger --------------------------------------------------
        [2023-04-05 00:43:19,948] - INFO     ticket_feeder_logger - Checking '2-CodeBuild-entries.json' contains requested values: ['title', 'link']
        [2023-04-05 00:43:19,948] - INFO     ticket_feeder_logger - All requested values ['title', 'link'] exist in '2-CodeBuild-entries.json'
        [2023-04-05 00:43:19,950] - INFO     ticket_feeder_logger - Checking 'templates/eks_release_template.json' contains specified placeholders: ['entries-placeholder', 'link-placeholder']
        [2023-04-05 00:43:19,950] - INFO     ticket_feeder_logger - Found placeholders: ['entries-placeholder', 'link-placeholder'] in JSON file 'templates/eks_release_template.json'   
        [2023-04-05 00:43:19,951] - INFO     ticket_feeder_logger - Updating template 'templates/eks_release_template.json'. Replacing ['entries-placeholder', 'link-placeholder'] with ['title', 'link']
        [2023-04-05 00:43:19,952] - INFO     ticket_feeder_logger --------------------------------------------------
        [2023-04-05 00:43:20,983] - INFO     jira_issue_creator - Ticket created: {"id":"10297","key":"ISS-290","self":"https://itsham-sajid.atlassian.net/rest/api/3/issue/10297"}
        [2023-04-05 00:43:21,901] - INFO     jira_issue_creator - Ticket created: {"id":"10298","key":"ISS-291","self":"https://itsham-sajid.atlassian.net/rest/api/3/issue/10298"}
        [2023-04-05 00:43:21,902] - INFO     jira_issue_creator - Total tickets created: 2
        [2023-04-05 00:43:21,902] - INFO     ticket_feeder_logger --------------------------------------------------


