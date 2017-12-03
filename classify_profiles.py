#!/usr/bin/env python3.5

"""Goes through all tags and collects their information"""
import json
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
#chrome_options.add_argument('--headless')
chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en-US'})
browser = webdriver.Chrome('./assets/chromedriver', chrome_options=chrome_options)

# makes sure slower connections work as well
browser.implicitly_wait(25)

try:
  json_file = open('./logs/classified_profiles_{}.json'.format(datetime.now()), 'a+')
  classified_profiles = []
  tags = get_all_tags()

  for tag in tags:
    print('Getting usernames from {0}'.format(tag))
    usernames = get_usernames_from_tag(tag)

    for username in usernames:
      print('Extracting information from {0}'.format(username))
      user_info = extract_information(browser, username)
      #classified_profiles.append()

      json_file.write('{0},\n'.format(json.dumps(user_info, indent=4)))

  # print('Writing classified results to file')
  # with open('./logs/classified_profiles_{}.json'.format(datetime.now()), 'w+') as fp:

  print('Done')

except KeyboardInterrupt:
  print('Aborted...')

finally:
  browser.delete_all_cookies()
  browser.close()
  json_file.close()
