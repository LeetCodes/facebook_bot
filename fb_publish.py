from facebot import Facebook
from random import shuffle, randint

import facebook
import fbconsole
import requests
import json
import time
import re
from datetime import datetime, date, timedelta
from bs4 import BeautifulSoup, Comment

import fb_group_except_list


def get_access_token_expired_time(token):
  token_verified_url = 'https://graph.facebook.com/oauth/access_token_info?client_id=145634995501895&access_token={}'
  url = token_verified_url.format(token)
  r = requests.get(url)
  content = json.loads(r.text)
  try:
    expired = content['expires_in']
    return expired
  except:
    return 0

def get_access_token(username, password):
  f = Facebook(username, password)
  return f.get_access_token()

def get_fb_graph_instance(token):
  return facebook.GraphAPI(access_token=token, version='2.3')

def get_fb_groups(graph):
  groups = graph.get_object('/me/groups')
  group_list = list(fbconsole.iter_pages(groups))
  # group_list_hookfunction(group_list)
  return group_list

def get_fb_random_groups(graph):
  groups_list = get_fb_groups(graph)
  shuffle(groups_list)
  return groups_list


# def group_list_hookfunction(group_list):
  # return
  # group_list = fb_group_except_list.FACEBOOK_GROUP_EXCEPT_LIST

def print_group(groups):
  for g in groups:
    print (g)

def publish_to_fb_group(graph, group_list, token):
  while(True):
    if (len(group_list) == 0):
      print('facebook groups list has been empty\n')
      return 'GROUP_LIST_EMPTY'

    group_id = group_list[-1]['id']
    group_name = group_list[-1]['name']
    group_list.pop(-1)

    art_id= randint(post_id_start, post_id_end)
    art_link = 'http://www.dobee01.com/p/{}/'.format(art_id)

    token_time = get_access_token_expired_time(token)
    print('token expired time = ', token_time)
    if (token_time < (60 * 8 + 120)) :
      return 'ACCESS_TOKEN_TIME_EXPIRED' 

    fb_post_id = 0
    try:
      attachment = {'link' : art_link}
      message = '喜歡我的文章，請來我的粉絲團按讚關注我們。\n https://www.facebook.com/dobee01/'
      # res = graph.put_wall_post(message="test", attachment = {'link':'http://www.dobee01.com/p/3111/'}, profile_id = '277936995586328')
      # fb_post_id = graph.put_object(parent_object=group_id, connection_name='feed', message = message, link=art_link)
      # fb_post_id = graph.put_wall_post(message = message, attachment = {'link':art_link})
      fb_post_id = graph.put_wall_post(message = message, attachment = {'link':art_link}, profile_id = group_id)
      print(current_time(), fb_post_id, ' publish_to ', group_id, group_name, art_link, ' sleeping 8 minutes\n')
      time.sleep(60 * 8)
    except:
      print(current_time(), fb_post_id, ' publish error ', group_id, group_name, art_link, ' sleeping 1 minutes\n')
      time.sleep(60)
      pass

def publish_to_fb_group_comment(graph, group_list, token):
  while(True):
    if (len(group_list) == 0):
      print('facebook groups list has been empty\n')
      return 'GROUP_LIST_EMPTY'

    group_id = group_list[-1]['id']
    group_name = group_list[-1]['name']
    group_list.pop(-1)

    group_comments_id_0 = graph.get_object(group_id+"/feed")['data'][0]['id']
    group_comments_id_1 = graph.get_object(group_id+"/feed")['data'][1]['id']
    group_comments_id_2 = graph.get_object(group_id+"/feed")['data'][2]['id']
    group_comments_id_3 = graph.get_object(group_id+"/feed")['data'][3]['id']
    group_comments_id_4 = graph.get_object(group_id+"/feed")['data'][4]['id']

    
    token_time = get_access_token_expired_time(token)
    print('token expired time = ', token_time)
    if (token_time < (60 * 8 + 120)) :
      return 'ACCESS_TOKEN_TIME_EXPIRED' 

    fb_post_id = 0
    try:
      art_id= randint(post_id_start, post_id_end)
      art_link = 'http://www.dobee01.com/p/{}/'.format(art_id)
      message = art_link 
      fb_post_id = graph.put_object(parent_object=group_comments_id_0, connection_name='comments', message = message)
      title = get_article_title(art_link)
      print(current_time(), fb_post_id, ' publish_to ', group_id, group_name, art_link, title)
      time.sleep(20)

      art_id= randint(post_id_start, post_id_end)
      art_link = 'http://www.dobee01.com/p/{}/'.format(art_id)
      message = art_link 
      fb_post_id = graph.put_object(parent_object=group_comments_id_1, connection_name='comments', message = message)
      title = get_article_title(art_link)
      print(current_time(), fb_post_id, ' publish_to ', group_id, group_name, art_link, title)
      time.sleep(20)

      art_id= randint(post_id_start, post_id_end)
      art_link = 'http://www.dobee01.com/p/{}/'.format(art_id)
      message = art_link 
      fb_post_id = graph.put_object(parent_object=group_comments_id_2, connection_name='comments', message = message)
      title = get_article_title(art_link)
      print(current_time(), fb_post_id, ' publish_to ', group_id, group_name, art_link, title)
      time.sleep(20)

      art_id= randint(post_id_start, post_id_end)
      art_link = 'http://www.dobee01.com/p/{}/'.format(art_id)
      message = art_link 
      fb_post_id = graph.put_object(parent_object=group_comments_id_3, connection_name='comments', message = message)
      title = get_article_title(art_link)
      print(current_time(), fb_post_id, ' publish_to ', group_id, group_name, art_link, title)
      time.sleep(20)

      art_id= randint(post_id_start, post_id_end)
      art_link = 'http://www.dobee01.com/p/{}/'.format(art_id)
      message = art_link 
      fb_post_id = graph.put_object(parent_object=group_comments_id_4, connection_name='comments', message = message)
      title = get_article_title(art_link)
      print(current_time(), fb_post_id, ' publish_to ', group_id, group_name, art_link, title)
      time.sleep(20)

      print('sleeping 5 mins\n')
      time.sleep(60 * 10)
    except:
      print(current_time(), fb_post_id, ' publish error ', group_id, group_name, art_link, ' sleeping 1 minutes\n')
      time.sleep(60)
      pass

def welcome_login_fb(graph):
  me = graph.get_object('/me')
  print(me['name'], 'welcome back\n')

def current_time():
  return '[' + (datetime.now()).strftime('%Y/%m/%d %H:%M:%S') + ']'

def get_article_title(url):
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'lxml')
  title = re.sub(r'[-, So, Funny, Easy]', '', soup.title.text)
  return title



username = 'wangcandy700120@gmail.com'
password = '0228345105'

# 2650 ~ 3279
post_id_start = 10400
post_id_end   = 10503 

reget_token = True
reget_group_list = True

status = 0
while(True):
  if (reget_token == True):
    token = get_access_token(username, password)
    graph = get_fb_graph_instance(token)
    welcome_login_fb(graph)
    reget_token = False


  if (reget_group_list == True):
    group_list = get_fb_random_groups(graph)
    reget_group_list = False

  try:
    status = publish_to_fb_group_comment(graph, group_list, token)
  except:
    pass

  if (status == 'ACCESS_TOKEN_TIME_EXPIRED'):
    reget_token = True
  elif (status == 'GROUP_LIST_EMPTY'):
    reget_group_list = True
  else:
    reget_token = True
    reget_group_list = True




