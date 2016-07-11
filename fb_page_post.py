from facebot import Facebook

import facebook
import fbconsole
import requests
import json
import time
import re
from datetime import datetime, date, timedelta
from random import shuffle, randint
from bs4 import BeautifulSoup, Comment

def sleep_time(seconds, count_down_msg = 'YES'):
  pause_sec = seconds
  while seconds >= 0:
    if count_down_msg == 'YES':
      print('pause %s seconds....   Count down = %04s' %(pause_sec, seconds), end = '\r')
    time.sleep(1)
    seconds = seconds - 1

  if count_down_msg == 'YES':
    print(end = '\n')

def rand_sleep_time(rand_start, rand_end, count_down_msg = 'YES'):
  rand_num = randint(rand_start, rand_end)
  sleep_time(rand_num, count_down_msg)


def get_access_token_expired_time(token):
  token_verified_url = 'https://graph.facebook.com/oauth/access_token_info?client_id=145634995501895&access_token={}'
  url = token_verified_url.format(token)
  r = requests.get(url)
  content = json.loads(r.text)
  try:
    return content['expires_in']
  except:
    return 0

def get_access_token(username, password):
  f = Facebook(username, password)
  return f.get_access_token()

def get_fb_page_token(username, password):
  token = get_access_token(username, password)
  graph = facebook.GraphAPI(access_token=token, version='2.3')
  accounts = graph.get_object('/me/accounts')

  fb_page_count = len(accounts['data'])
  if fb_page_count == 1:
    page_token = accounts['data'][0]['access_token']
    page_id    = accounts['data'][0]['id']
    page_name  = accounts['data'][0]['name']
  else:
    number = 1
    for page_info in accounts['data']:
      print('No.{} {}'.format(number, page_info['name']))
      number += 1

    while(True):
      choice_num = input('input the number (input \'q\' to quit): ')
      if (choice_num == 'q'):
        raise NameError('quit select category')
      choice_num = int(choice_num)
      if (choice_num < 0) or (choice_num > category_count):
        print('please input a correct category number')
      else:
        choice_num = choice_num - 1
        page_token = accounts['data'][choice_num]['access_token']
        page_id    = accounts['data'][choice_num]['id']
        page_name  = accounts['data'][choice_num]['name']
        break
  return page_id, page_token

def get_fb_page_graph_instance(username, password):
  page_id, page_token = get_fb_page_token(username, password)
  page_graph = facebook.GraphAPI(page_token)
  return page_graph

def current_time():
  return '[' + (datetime.now()).strftime('%Y/%m/%d %H:%M:%S') + ']'

def get_article_title(url):
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'lxml')
  title = re.sub(r'[-, So, Funny, Easy]', '', soup.title.text)
  return title



username = input('Input Username:')
password = input('Input Password:')

art_start_no = 11257
art_end_no   = 11271

page_id, page_token = get_fb_page_token(username, password)
page_graph = facebook.GraphAPI(page_token)
# dobee01_id = '1020239824709036'

for post_id in range(art_start_no, art_end_no + 1):
  expired_time = get_access_token_expired_time(page_token)
  if (expired_time < (60)):
    print('Page Token is expired, prepare to reget page token\n')
    while(True):
      try:
        page_graph = get_fb_page_graph_instance(username, password)
        break
      except:
        sleep_time(10)
        continue

  art_link = 'http://www.dobee01.com/p/{}/?r=fb_page'.format(post_id)
  title    = get_article_title(art_link)
  try:
    post_id = page_graph.put_object(parent_object = page_id, connection_name='feed', link=art_link, message=title)
    print(current_time(), title, art_link, 'has been publish to dobee01 page, prepare sleep, post_id = ', post_id)
    sleep_time(600)
  except Exception as exc:
    print(exc)
    print(current_time(), art_link, 'has somthing wrong to publish dobee01 facebook page\n')
    sleep_time(3)
    pass









