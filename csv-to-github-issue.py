import configparser
import argparse
import csv
import requests
import json

CONFIG_FILE = 'csv-to-github-issue.config'
GH_API_URL = 'https://api.github.com'

def parse_args():
    parser = argparse.ArgumentParser(description='Upload CSV (title,description) of issues to GitHub repository.')
    parser.add_argument('file', metavar='csv', type=str, help='the CSV file of issues to upload')
    args = parser.parse_args()
    return args

def parse_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    options = dict(config[config.default_section])
    return options

def read_csv(filename):
    file = open(filename, 'r')
    rows = csv.reader(file)
    return rows

def push_issues(repo_owner, repo, issues, user, token):
    url = "{}/repos/{}/{}/issues".format(GH_API_URL, repo_owner, repo)
    #Accept: application/vnd.github.v3+json
    headers = {'Accept': 'application/vnd.github.v3+json'}
    auth = (user, token)
    for issue in issues:
        data = {'title': issue[0], 'body': issue[1]}
        r = requests.post(url, data=json.dumps(data), auth=auth, headers=headers)

def main():
    options = parse_config()
    args = parse_args()
    file = args.file
    issues = read_csv(file)
    push_issues(options['repo_owner'], options['repo'], issues, options['user'], options['token'])

if __name__ == '__main__':
    main()