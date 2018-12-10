"""Methods to extract the data for the given usernames profile"""
from functools import reduce
from time import sleep
from re import findall

import requests
from selenium.common.exceptions import WebDriverException
import os

windows_os = os.name == 'nt'




def get_usernames_from_tag(tag):
    """Retruns a list of usernames that were found for that tag"""
    try:
        tag_url = 'https://www.instagram.com/explore/tags/{0}/?__a=1'.format(tag)
        tag_res = requests.get(tag_url).json()

        nodes = tag_res['graphql']['hashtag']['edge_hashtag_to_media']['edges']

        new_urls = [node['node']['shortcode'] for node in nodes]
        new_req = [requests.get('https://www.instagram.com/p/{0}/?__a=1'.format(url)).json() for url in new_urls]

        usernames = [req['graphql']['shortcode_media']['owner']['username'] for req in new_req]

        return usernames

    except Exception as err:
        print('{0} - Skipping tag {1}...'.format(str(err), tag))
        return []


def getUserData(query,
                browser,
                basequery="return window._sharedData.entry_data.ProfilePage[0]."):
    try:
        data = browser.execute_script(
            basequery + query)
        return data
    except WebDriverException:
        browser.execute_script("location.reload()")

        data = browser.execute_script(
            basequery + query)
        return data


def extract_information(browser, username):
    """Get all the information for the given username"""
    try:
        profile_url = 'https://www.instagram.com/{0}'.format(username)
        # browser.get(profile_url)
        browser.get(profile_url)

        if windows_os:
            import msvcrt
            print('Please enter sex:', end="", flush=True)
            sex = msvcrt.getwch()
            print('')
        else:
            sex = input('Please enter sex:')
            print('')
        # print(sex)

        profile = getUserData('graphql', browser)

        user = profile['user']
        media = user['edge_owner_to_timeline_media']
        nodes = media['edges']

        information = {
            'username': user.get('username', None),
            'full_name': user.get('full_name', None),
            'fb_connected': user.get('connected_fb_page', None),
            'follower': user['edge_followed_by']['count'],
            'follows': user['edge_follow']['count'],
            'biography': user.get('biography', None),
            'num_of_posts': media.get('count', None),
            'num_of_videos': len([node for node in nodes if node['node']['__typename'] != 'GraphImage']),
            'posts': [{
                'caption': node['node']['edge_media_to_caption']['edges'][0]['node'].get('text', None) or None,
                'num_of_comments': node['node']['edge_media_to_comment']['count'],
                'num_of_likes': node['node']['edge_liked_by']['count']
            } for node in nodes],
            'sex': sex
        }

        return information

    except Exception as err:
        print('{0} - This account was not classified...'.format(str(err)))
        return {}
