#!/usr/bin/env python3.5

"""Goes through all tags and collects their information"""
import json
import os
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from util.cli_helper import get_all_tags
from util.extractor import extract_information
from util.extractor import get_usernames_from_tag

chrome_options = Options()
chrome_options.add_argument('--dns-prefetch-disable')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--lang=en-US')
# chrome_options.add_argument('--headless')
chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en-US'})
browser = webdriver.Chrome('./assets/chromedriver', chrome_options=chrome_options)

# makes sure slower connections work as well
browser.implicitly_wait(25)


def rotate_number(prefix, suffix):
    i = 1
    while os.path.exists(prefix + str(i) + suffix):
        i += 1
    return i


def getAllUsers(path):
    usernameSet = set()
    for f in os.listdir(path):
        if f.startswith('classified_profiles_'):
            try:
                with open(os.path.join(path, f), 'r') as t:
                    # print(t.read())
                    d = json.loads(t.read())
                    # print(d)
                for o in d:
                    # print(o)
                    if 'username' in list(o.keys()):
                        usernameSet.add(o['username'])
            except Exception as e:
                print('{} - Skipping {}'.format(str(e),f))
    return usernameSet


default_number_of_users_per_tag = 10


def loadUsernames(tag):
    with open('./logs/{}.json'.format(tag), 'r') as f:
        return json.load(f)


def logUsernamesForTag(data, tag):
    with open('./logs/{}.json'.format(tag), 'w') as f:
        json.dump(data, f)


try:
    logged_users = getAllUsers('./logs/')
    json_file = open('./logs/classified_profiles_{}.json'.format(rotate_number('./logs/classified_profiles_', '.json')),
                     'a+')
    json_file.write('[')

    classified_profiles = []
    tags = get_all_tags()

    for tag in tags:
        print('Getting usernames from {0}'.format(tag))

        try:
            allUsernames = loadUsernames(tag)
            if len(allUsernames) < default_number_of_users_per_tag:
                raise Exception('Not enough usernames')
        except Exception as e:
            allUsernames = get_usernames_from_tag(tag)

        maxLen = min(len(allUsernames), default_number_of_users_per_tag)
        usernames = allUsernames[0:maxLen]
        logUsernamesForTag(allUsernames[maxLen:], tag)

        for username in usernames:
            if username in logged_users:
                print('Skipping @{} ...'.format(username))
            else:
                print('Extracting information from {0}'.format(username))
                user_info = extract_information(browser, username)

                json_file.write('{0},\n'.format(json.dumps(user_info, indent=4)))
                logged_users.add(username)

    # print('Writing classified results to file')
    # with open('./logs/classified_profiles_{}.json'.format(datetime.now()), 'w+') as fp:

    print('Done')


except KeyboardInterrupt:
    print('Aborted...')

finally:
    if 'json_file' in locals():
        json_file.write("{}]")
        json_file.close()
    if browser:
        browser.delete_all_cookies()
        browser.close()
