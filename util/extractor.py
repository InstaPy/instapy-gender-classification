"""Methods to extract the data for the given usernames profile"""
from functools import reduce
from time import sleep
from re import findall

import requests

def get_usernames_from_tag(tag):
  """Retruns a list of usernames that were found for that tag"""
  try:
    tag_url = 'https://www.instagram.com/explore/tags/{0}/?__a=1'.format(tag)
    tag_res = requests.get(tag_url).json()

    nodes = tag_res['tag']['media']['nodes']

    new_urls = [node['code'] for node in nodes]
    new_req = [requests.get('https://www.instagram.com/p/{0}/?__a=1'.format(url)).json() for url in new_urls]

    usernames = [req['graphql']['shortcode_media']['owner']['username'] for req in new_req]

    return usernames

  except Exception as err:
    return []

def extract_information(browser, username):
  """Get all the information for the given username"""
  try:
    profile_url = 'https://www.instagram.com/{0}'.format(username)
    browser.get(profile_url)

    sex = input('Please enter sex:')
    print(sex)

    profile = requests.get('{0}{1}'.format(profile_url, '/?__a=1')).json()

    user = profile['user']
    media = user['media']
    nodes = media['nodes']

    information = {
      'username': user.get('username', None),
      'full_name': user.get('full_name', None),
      'fb_connected': user.get('connected_fb_page', None),
      'follower': user['followed_by']['count'],
      'follows': user['follows']['count'],
      'biography': user.get('biography', None),
      'num_of_posts': media.get('count', None),
      'num_of_videos': len([node for node in nodes if node['is_video']]),
      'posts': [{
                  'caption': node.get('caption', None),
                  'num_of_comments': node['comments']['count'],
                  'num_of_likes': node['likes']['count']
                } for node in nodes],
      'sex': sex
    }

    return information

  except Exception as err:
    return {}