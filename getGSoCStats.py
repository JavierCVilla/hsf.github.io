import os
import pandas as pd
import re

PROJECTS_DIR  = "_gsocprojects"
PROPOSALS_DIR = "_gsocproposals"
ORGS_DIR      = "_gsocorgs"

columns_project = ["Name", "Year"]
columns_prop    = ["Project", "Organization", "Year", "Title"]
columns_org     = ["Name", "Year"]

projects  = pd.DataFrame(columns=columns_project)
proposals = pd.DataFrame(columns=columns_prop)
orgs      = pd.DataFrame(columns=columns_org)

project_name_re      = "project: (.*)\n"
organization_name_re = "organization: (.*)\n"
proposal_name_re     = "title:\s*\"?(.*)\"?\n"
proposal_project_re  = "project:\s*(.*)\n"
proposal_org_re      = "organization:[\n| ]([\s\-\w]*)---"

for year in ['2017', '2018', '2019'] :
    # Get projects
    for p in os.listdir(os.path.join(PROJECTS_DIR, year)):
        with open(os.path.join(PROJECTS_DIR, year, p)) as f:
            result = re.search(project_name_re, f.read())
            projects.loc[len(projects)] = [result.group(1), year]

    # Get orgs
    for p in os.listdir(os.path.join(ORGS_DIR, year)):
        with open(os.path.join(ORGS_DIR, year, p)) as f:
            result = re.search(organization_name_re, f.read())
            orgs.loc[len(orgs)] = [result.group(1), year]

    # Get proposals
    for p in os.listdir(os.path.join(PROPOSALS_DIR, year)):
        with open(os.path.join(PROPOSALS_DIR, year, p)) as f:
            if p.startswith("proposal_"):
                content = f.read()
                title = re.search(proposal_name_re, content).group(1)
                try:
                    project = re.search(proposal_project_re, content).group(1)
                except:
                    project = "NA"
                org = re.search(proposal_org_re, content).group(1)
                org_split = org.replace("- ", "").replace(" - ", "").rstrip("\n").split("\n")
                org_string = ", ".join(filter(None, org_split))
                proposals.loc[len(proposals)] = [project, org_string, year, title]

proposals.to_csv(r'proposals.csv')
