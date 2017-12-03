"""Util functions for the script"""
import sys

def get_all_tags():
  """Returns all the tags given as parameter"""
  tags = []

  #display provide username
  if len(sys.argv) < 2:
    sys.exit('- Please provide at least one tag!\n')

  for username in sys.argv[1:]:
    tags.append(username)

  return tags
