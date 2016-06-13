from facebot import Facebook
from random import shuffle, randint

import facebook
import fbconsole
import requests
import json
import time
import re
import requests
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

def get_fb_search_result_list(graph, query_word, query_type):
  # query_type
  # user
  # 搜尋用戶（如果用戶允許搜尋名稱）。
  # 名稱。
  #
  # page
  # 搜尋粉絲專頁。
  # 名稱。
  #
  # event
  # 搜尋活動。
  # 名稱。
  #
  # group
  # 搜尋社團。
  # 名稱。
  #
  # place
  # 搜尋地標。您可以新增 center 參數（含經緯度）和選用的 distance 參數（以公尺計），將搜尋範圍縮小至特定地點和距離：
  # 名稱。
  #
  # placetopic
  # 傳回可能的地標粉絲專頁主題和編號的清單。使用 topic_filter=all 參數以取得完整清單。
  # 無。
  #
  # ad_*
  # 不同搜尋選項的集合，可用於找出目標設定選項。
  # 請參閱目標設定選項文件
  search_result = graph.request('/search?', {'q':query_word, 'type':query_type, 'limit':20})
  search_list = list(fbconsole.iter_pages(search_result))
  return search_list

def dump_fb_search_list(search_list):
  for search in search_list:
    page_name = search['name']
    page_id   = search['id']
    page_detail = graph.get_object(page_id)
    page_like_count = page_detail['likes']
    if (page_like_count < 15000):
      continue
    print(page_id, page_name, 'likes {}'.format(page_like_count))

def get_fb_page_token(username, password):
  token = get_access_token(username, password)
  graph = facebook.GraphAPI(access_token=token, version='2.3')
  accounts = graph.get_object('/me/accounts')
  page_token = accounts['data'][0]['access_token']
  return page_token

def get_fb_page_graph_instance(username, password):
  page_token = get_fb_page_token(username, password)
  page_graph = facebook.GraphAPI(page_token)
  return page_graph


  

username = 'tittan0829@gmail.com'
password = 'Novia0829'

# 2650 ~ 3279
post_id_start = 10870
post_id_end   = 10905

reget_token = True
reget_group_list = True

token = get_fb_page_token(username, password)
graph = get_fb_graph_instance(token)
welcome_login_fb(graph)

# search_list = get_fb_search_result_list(graph, '好文', "page")
# dump_fb_search_list(search_list[:20])

# search_list = get_fb_search_result_list(graph, '心情', "page")
# dump_fb_search_list(search_list[:20])

comment = graph.get_object('417506414983829/feed')
comment_id = comment['data'][0]['id']
print(comment_id)


message = '謝謝分享，感恩'
fb_post_id = graph.put_object(parent_object=comment_id, connection_name='comments', message = message)
