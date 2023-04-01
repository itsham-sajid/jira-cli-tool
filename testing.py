import json

newvalues = {'Entry 1': {'published': 'Thu, 30 Mar 2023 17:13:08 +0000', 'title': 'AWS Batch now supports user-defined pod labels on Amazon EKS', 'link': 'https://aws.amazon.com/about-aws/whats-new/2023/03/aws-batch-user-defined-pod-labels-amazon-eks/'}, 'Entry 2': {'published': 'Thu, 30 Mar 2023 22:09:43 +0000', 'title': 'Amazon GuardDuty now monitors runtime activity from containers running on Amazon EKS', 'link': 'https://aws.amazon.com/about-aws/whats-new/2023/03/amazon-guardduty-monitors-runtime-activity-containers-eks/'}, 'Entry 3': {'published': 'Mon, 27 Mar 2023 21:50:31 +0000', 'title': 'Amazon EKS adds domainless gMSA authentication for Windows containers', 'link': 'https://aws.amazon.com/about-aws/whats-new/2023/03/amazon-eks-domainless-gmsa-authentication-windows-containers/'}}

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



def update_dict(newvalues, templatefile, field_list):
    new_templates = []

    placeholders = ['title-placeholder', 'link-placeholder']

    for key, value in newvalues.items():
        extracted_values = [value[field] for field in field_list]
        with open(templatefile, 'r') as f:
            template = json.load(f)
            new_template = update_placeholders(template, placeholders, extracted_values)
            new_templates.append(new_template)

    return new_templates


templatefile = "template.json"
requested_values = ['title', 'link']
new_templates = update_dict(newvalues, templatefile, requested_values)

print(new_templates)