from facebot import Facebook
from random import shuffle, randint

import facebook
import fbconsole
import requests
import json
import time
import re
import configparser
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
  global article_pub_count
  while(True):
    if (len(group_list) == 0):
      print('facebook groups list has been empty\n')
      return 'GROUP_LIST_EMPTY'
    
    token_time = get_access_token_expired_time(token)
    welcome_login_fb(graph)
    print('token expired time = ', token_time)
    if (token_time < (60 * 5)) :
      print('token has been expired')
      return 'ACCESS_TOKEN_TIME_EXPIRED'
      # token = get_access_token(username, password)
      # graph = get_fb_graph_instance(token)

    group_id = group_list[0]['id']
    group_name = group_list[0]['name']
    group_list.pop(0)

    art_id= randint(post_id_start, post_id_end)
    art_link = 'http://www.dobee01.com/p/{}/'.format(art_id)

    fb_post_id = 0
    try:
      attachment = {'link' : art_link}
      title      = get_article_title(art_link)
      message    = title + '\n' + art_link
      # res = graph.put_wall_post(message="test", attachment = {'link':'http://www.dobee01.com/p/3111/'}, profile_id = '277936995586328')
      fb_post_id = graph.put_object(parent_object=group_id, connection_name='feed', message = message, link=art_link)
      # fb_post_id = graph.put_wall_post(message = message, attachment = {'link':art_link})
      # fb_post_id = graph.put_wall_post(message = message, attachment = {'link':art_link}, profile_id = group_id)
      print('No.{}'.format(article_pub_count), current_time(), fb_post_id, ' publish_to ', group_id, group_name, art_link, title, 'group count = ', len(group_list))
    except Exception as exc:
      print('publish_to_fb_group(), post exception = ', exc)
      print(current_time(), fb_post_id, ' publish error ', group_id, group_name, art_link, 'group count = ', len(group_list))
      sleep_time(5)

    if (fb_post_id == 0):
      continue

    try:
      message = '按個讚加入粉絲團支持我們，給我們個鼓厲\n https://www.facebook.com/dobee01/'
      fb_post_id = graph.put_object(parent_object=fb_post_id['id'], connection_name='comments', message = message)
      print('No.{}'.format(article_pub_count), current_time(), fb_post_id, ' comment_to ', group_id, group_name, message)
    except Exception as exc:
      print('publish_to_fb_group(), comment exception = ', exc)
      print(current_time(), fb_post_id, 'comment error ', group_id, group_name, art_link)
      pass

    if (article_pub_count % 10 == 0):
      rand_sleep_time(60*25, 60*30)
    else:
      rand_sleep_time(12, 24)
    article_pub_count += 1
    print('===================================================================================================')

def publish_to_fb_group_comment(graph, group_list, token):
  global article_pub_count
  while(True):
    token_time = get_access_token_expired_time(token)
    welcome_login_fb(graph)
    print('token expired time = ', token_time)
    if (token_time < (60 * 8 + 120)) :
      print('token has been expired')
      return 'ACCESS_TOKEN_TIME_EXPIRED'
      # token = get_access_token(username, password)
      # graph = get_fb_graph_instance(token)

    if (len(group_list) == 0):
      print('facebook groups list has been empty\n')
      return 'GROUP_LIST_EMPTY'

    group_id = group_list[0]['id']
    group_name = group_list[0]['name']
    group_list.pop(0)

    group_comments_id_list = list()
    for idx in range(0,5):
      group_comments_id = graph.get_object(group_id+"/feed")['data'][idx]['id']
      group_comments_id_list.append(group_comments_id)

    fb_post_id = 0
    try:
      for group_comments_id in group_comments_id_list:
        art_id= randint(post_id_start, post_id_end)
        art_link = 'http://www.dobee01.com/p/{}/'.format(art_id)
        title = get_article_title(art_link)
        message = title + '\n' + art_link 
        fb_post_id = graph.put_object(parent_object=group_comments_id, connection_name='comments', message = message)
        
        message = '按個讚加入粉絲團支持我們，給我們個鼓厲\n https://www.facebook.com/dobee01/'
        fb_post_id = graph.put_object(parent_object=group_comments_id, connection_name='comments', message = message)
        print('No.{}'.format(article_pub_count) ,current_time(), fb_post_id, ' publish_to ', group_id, group_name, art_link, title, ' group count = ', len(group_list))
        rand_sleep_time(5, 10, 'No')
    except Exception as exc:
      print('publish_to_fb_group_comment(), exception = ', exc)
      print('No.{}'.format(article_pub_count), current_time(), fb_post_id, ' publish error ', group_id, group_name, art_link, ' group count = ', len(group_list))
      pass

    if (article_pub_count % 50 == 0):
      rand_sleep_time(60*10, 60*15)
    else:
      rand_sleep_time(12, 24)
    article_pub_count += 1
    print('===================================================================================================')


def welcome_login_fb(graph):
  me = graph.get_object('/me')
  print(me['name'], 'welcome back')

def current_time():
  return '[' + (datetime.now()).strftime('%Y/%m/%d %H:%M:%S') + ']'

def get_article_title(url):
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'lxml')
  title = re.sub(r'[-, So, Funny, Easy]', '', soup.title.text)
  return title

def get_fb_setting_info():
  config = configparser.ConfigParser()
  config.read('fb_setting_info.ini')
  return config

def get_account_info_list():
  config = get_fb_setting_info()
  account_list = list()
  for k in config['ACCOUNT_INFO']:
    tmp = [k, config['ACCOUNT_INFO'][k]] 
    account_list.append(tmp)
  return account_list

def get_user_and_pass_from_list():
  global account_list
  global account_list_len
  global account_idx
  username = account_list[account_idx][0]
  password = account_list[account_idx][1]
  account_idx += 1
  if (account_idx == account_list_len):
    account_idx = 0
  return username, password


config = get_fb_setting_info()

account_list     = get_account_info_list()
account_list_len = len(account_list)
account_idx      = 0

# 2650 ~ 3279
post_id_start = int(config['ARTICLE_ID']['start'])
post_id_end   = int(config['ARTICLE_ID']['end'])

reget_token = True
reget_group_list = True

status = 0
article_pub_count = 1
while(True):
  if (reget_token == True):
    username, password = get_user_and_pass_from_list()
    token = get_access_token(username, password)
    graph = get_fb_graph_instance(token)
    reget_token = False

  if (reget_group_list == True):
    token_time = get_access_token_expired_time(token)
    if (token_time <= 60):
      username, password = get_user_and_pass_from_list()
      token = get_access_token(username, password)
      graph = get_fb_graph_instance(token)
    group_list = get_fb_random_groups(graph)
    reget_group_list = False

  try:
    status = publish_to_fb_group(graph, group_list, token)
    # status = publish_to_fb_group_comment(graph, group_list, token)
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




