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
  article_pub_count = 1
  while(True):
    if (len(group_list) == 0):
      print('facebook groups list has been empty\n')
      return 'GROUP_LIST_EMPTY'
    
    token_time = get_access_token_expired_time(token)
    print('token expired time = ', token_time)
    if (token_time < (60 * 5 + 120)) :
      token = get_access_token(username, password)
      graph = get_fb_graph_instance(token)

    group_id = group_list[-1]['id']
    group_name = group_list[-1]['name']
    group_list.pop(-1)

    art_id= randint(post_id_start, post_id_end)
    art_link = 'http://www.dobee01.com/p/{}/'.format(art_id)

    fb_post_id = 0
    try:
      attachment = {'link' : art_link}
      title      = get_article_title(art_link)
      message    = title + '\n' + art_link
      # res = graph.put_wall_post(message="test", attachment = {'link':'http://www.dobee01.com/p/3111/'}, profile_id = '277936995586328')
      # fb_post_id = graph.put_object(parent_object=group_id, connection_name='feed', message = message, link=art_link)
      # fb_post_id = graph.put_wall_post(message = message, attachment = {'link':art_link})
      fb_post_id = graph.put_wall_post(message = message, attachment = {'link':art_link}, profile_id = group_id)
      print(article_pub_count, current_time(), fb_post_id, ' publish_to ', group_id, group_name, art_link, title)

      message = '按個讚加入粉絲團支持我們，給我們個鼓厲\n https://www.facebook.com/dobee01/\n'
      fb_post_id = graph.put_object(parent_object=fb_post_id['id'], connection_name='comments', message = message)
      print(article_pub_count, current_time(), fb_post_id, ' comment_to ', group_id, group_name, message)
      article_pub_count += 1

      sleep_time = randint(60*2, 60*5)
      print('sleep time = ', sleep_time, 'group count = ', len(group_list))
      time.sleep(sleep_time)
    except Exception as exc:
      print('publish_to_fb_group(), exception = ', exc)
      print(current_time(), fb_post_id, ' publish error ', group_id, group_name, art_link, ' sleeping 1 minutes\n')
      time.sleep(60)
      pass

def publish_to_fb_group_comment(graph, group_list, token):
  article_pub_count = 0
  while(True):
    token_time = get_access_token_expired_time(token)
    print('token expired time = ', token_time)
    if (token_time < (60 * 8 + 120)) :
      token = get_access_token(username, password)
      graph = get_fb_graph_instance(token)

    if (len(group_list) == 0):
      print('facebook groups list has been empty\n')
      return 'GROUP_LIST_EMPTY'

    group_id = group_list[0]['id']
    group_name = group_list[0]['name']
    group_list.pop(0)

    group_comments_id_0 = graph.get_object(group_id+"/feed")['data'][0]['id']

    fb_post_id = 0
    try:
      art_id= randint(post_id_start, post_id_end)
      art_link = 'http://www.dobee01.com/p/{}/'.format(art_id)
      title = get_article_title(art_link)
      message = title + '\n' + art_link 
      fb_post_id = graph.put_object(parent_object=group_comments_id_0, connection_name='comments', message = message)
      
      message = '按個讚加入粉絲團支持我們，給我們個鼓厲\n https://www.facebook.com/dobee01/'
      fb_post_id = graph.put_object(parent_object=group_comments_id_0, connection_name='comments', message = message)
      print(article_pub_count ,current_time(), fb_post_id, ' publish_to ', group_id, group_name, art_link, title, ' group count = ', len(group_list))
      article_pub_count += 1
      rand_sleep_time(60 * 2, 60 * 5)
    except Exception as exc:
      print('publish_to_fb_group_comment(), exception = ', exc)
      print(current_time(), fb_post_id, ' publish error ', group_id, group_name, art_link, ' group count = ', len(group_list))
      rand_sleep_time(0, 60)
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
password = 'Novia0829'

# 2650 ~ 3279
post_id_start = 10900
post_id_end   = 10911

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
  except Exception as exc:
    print(current_time(), 'main function Exception = ', exc, ', status =', status)
    pass

  if (status == 'ACCESS_TOKEN_TIME_EXPIRED'):
    reget_token = True
  elif (status == 'GROUP_LIST_EMPTY'):
    reget_group_list = True
  else:
    reget_token = True
    reget_group_list = True




