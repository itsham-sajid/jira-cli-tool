import json

def update_placeholders(template, title, link):

    if isinstance(template, dict):
        newdict = {}
        for k, v in template.items():
            if isinstance(v, str):
                if v == "entries-placeholder":
                    newdict[k] = title
                elif v == "link-placeholder":
                    newdict[k] = link
                else:
                    newdict[k] = v
            else:
                newdict[k] = update_placeholders(v, title, link)
        return newdict
    elif isinstance(template, list):
        newlist = []
        for item in template:
            newlist.append(update_placeholders(item, title, link))
        return newlist
    else:
        return template



def update_dict(requested_entries, placeholders, templatefile):

    try:

        print(requested_entries, placeholders, templatefile)

        # formatted_templates = []

        # for key, value in newvalues.items():
        #     title = value['title']
        #     link = value['link']

            # with open(templatefile, 'r') as f:
            #     template = json.load(f)
            #     new_template = update_placeholders(template, title, link)
            #     formatted_templates.append(new_template)

        # return formatted_templates

    except Exception as e:
        print(f"\nERROR - An error occurred in __main__(): \n{e}")


