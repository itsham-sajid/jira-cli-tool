import json
from main import log_exception
import logging

logger = logging.getLogger(__name__)

@log_exception
def read_json_data_file(json_data, jira_template, req_values, template_placeholders):

    with open(json_data, 'r') as f:
        data = json.load(f)

    new_templates = []

    for key, value in data.items():
        extracted_values = [value[field] for field in req_values]
        with open(jira_template, 'r') as f:
            template = json.load(f)
            new_template = update_template_placeholders(template,  template_placeholders, extracted_values)
            new_templates.append(new_template)

    return new_templates

@log_exception
def update_template_placeholders(template, placeholders, requested_values):

    if isinstance(template, dict):
        newdict = {}
        for k, v in template.items():
            if isinstance(v, str):
                for i, placeholder in enumerate(placeholders):
                    if placeholder in v:
                        newvalue = v.replace(placeholder, requested_values[i])
                        break
                else:
                    newvalue = v
                newdict[k] = newvalue
            else:
                newdict[k] = update_template_placeholders(v, placeholders, requested_values)
        return newdict
    elif isinstance(template, list):
        newlist = []
        for item in template:
            newlist.append(update_template_placeholders(item, placeholders, requested_values))
        return newlist
    else:
        return template
