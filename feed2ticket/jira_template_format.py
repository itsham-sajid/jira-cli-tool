import json

def update_placeholders(template, placeholders, requested_values):

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
                newdict[k] = update_placeholders(v, placeholders, requested_values)
        return newdict
    elif isinstance(template, list):
        newlist = []
        for item in template:
            newlist.append(update_placeholders(item, placeholders, requested_values))
        return newlist
    else:
        return template



def update_dict(newvalues, templatefile, field_list, placeholders):

    print(newvalues, templatefile, field_list, placeholders)

    new_templates = []

    for key, value in newvalues.items():
        extracted_values = [value[field] for field in field_list]
        with open(templatefile, 'r') as f:
            template = json.load(f)
            new_template = update_placeholders(template, placeholders, extracted_values)
            new_templates.append(new_template)

    return new_templates