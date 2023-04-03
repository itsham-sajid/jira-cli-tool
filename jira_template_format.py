import json


def check_json_extension(json_data_file, values):

    checks_passed = False

    with open(json_data_file, "r") as f:
        data = json.load(f)

    if not json_data_file.endswith('.json'):
        raise ValueError('Error: JSON file required')
    else:
        file_type = True
        for key, value in data.items():
            if not all(item in value for item in values):
                print(f"Not all search values exist.\nPlease check JSON objects in '{json_data_file}' to make sure values {values} exist")
                checks_passed = False
                break
        else:
            print("All search values exist in the dictionary")
            checks_passed = True

    return checks_passed
  


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