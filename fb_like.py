from facebot import Facebook
from random import shuffle, randint, sample

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
  search_result = graph.request('/search?', {'q':query_word, 'type':query_type, 'limit':25})
  search_list = list(fbconsole.iter_pages(search_result))
  return search_list

def dump_fb_search_list(search_list, likes_count):
  for search in search_list:
    page_name = search['name']
    page_id   = search['id']
    page_detail = graph.get_object(page_id)
    page_like_count = page_detail['likes']
    if (page_like_count < likes_count):
      continue
    # print(page_id, page_name, 'likes {}'.format(page_like_count))
    yield page_id, page_name, page_like_count 

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

def strip_lines(string):
  tmp_str = str()
  for line in string.splitlines():
    if (line == ''):
      continue
    tmp_str.append(line)
  return tmp_str

def get_search_keyword_from_list(keyword_list):
  list_len = len(keyword_list)
  idx = 0
  for keyword in keyword_list:
    print('No.{} - {}'.format(idx, keyword))
    idx += 1

  while (True):
    select = input('input the number which you selected or \'q\' to exit program : ')
    if (select == 'q'):
      exit()
    else:
      select_no = int(select)
      if (select_no < 0) or (select_no >= list_len):
        continue
      else:
        print('you selected the %s' %(keyword_list[select_no]))
        return keyword_list[select_no]


def get_feed_list(graph, page_id, feed_limit):
  feed_list = graph.get_object(page_id+'/feed')
  tmp_list = []
  tmp_count = 0
  for feed in fbconsole.iter_pages(feed_list):
    tmp_list.append(feed)
    tmp_count += 1
    if (tmp_count > feed_limit):
      break
  return tmp_list

def get_comment_list(graph, feed_msg_id, comment_limit):
  feed_comment_list = graph.get_object(feed_msg_id + '/comments')
  tmp_list = []
  tmp_count = 0
  for comment in fbconsole.iter_pages(feed_comment_list):
    tmp_list.append(comment)
    tmp_count += 1
    if (tmp_count > comment_limit):
      break
  return tmp_list


# username = input('Input Username:')
# password = input('Input Password:')



reget_token = True
reget_group_list = True

token = get_fb_page_token(username, password)
graph = get_fb_graph_instance(token)
welcome_login_fb(graph)

search_keywords_list = [
    '東森新聞', 
    '蘋果日報', 
    'TVBS 新聞',
    '爆料公社',


]
search_keyword = get_search_keyword_from_list(search_keywords_list)
search_list = get_fb_search_result_list(graph, search_keyword, "page")

for page in search_list:
  page_name = page['name']
  if page_name == search_keyword:
    page_id = page['id']
    print(page)
    break;

feed_msg_no = 1
push_likes_count = 1

feed_list = get_feed_list(graph, page_id, 50)
for feed in feed_list:
  try:
    feed_msg = feed['message'].replace('\n', '')[0:30]
    feed_msg_id = feed['id']
    print('{} | No.{} | ({} | {})'.format(current_time(), feed_msg_no, feed_msg,feed_msg_id))
    feed_msg_no += 1
  except:
    continue

  try:
    feed_comment = get_comment_list(graph, feed_msg_id, 100) 
    # Add the element if like_count = 0
    feed_comment = [feed for feed in feed_comment if feed['like_count'] == 0]
    feed_total_comment_count = len(feed_comment)

    if (feed_total_comment_count <= 4):
      continue

    if (feed_total_comment_count >= 50):
      sample_count = int(feed_total_comment_count * 0.3)
    else:
      sample_count = int(feed_total_comment_count * 0.2)

    print('total_comment_count =', feed_total_comment_count, ' | prepare to like count =', sample_count)
    like_comment_id_list = sample(range(0, feed_total_comment_count), sample_count)
    for idx in like_comment_id_list:
      feed_comment_author     = feed_comment[idx]['from']['name']
      feed_comment_author_id  = feed_comment[idx]['from']['id']
      feed_comment_msg        = feed_comment[idx]['message'].replace('\n', '')[0:30]
      feed_comment_id         = feed_comment[idx]['id']
      feed_comment_like_count = feed_comment[idx]['like_count']
      fb_like_status         = graph.put_object(parent_object=feed_comment_id, connection_name='likes')
      print('\t', '{} |- No.{} ({}, {}) | {} | {} '.format(current_time(), idx, feed_comment_author_id, feed_comment_author, feed_comment_msg, feed_comment_id), 
                             '| push_likes_count =',push_likes_count)
      push_likes_count += 1
      rand_sleep_time(3, 8, 'No')
  except Exception as exc:
    print(exc)
    pass
  rand_sleep_time(6, 13)
  print('================================================================')


# for page_id, page_name, likes_count in dump_fb_search_list(search_list[:3], 100000):
  # print(page_id, page_name, likes_count)
  # feed_id = graph.get_object(page_id+'/feed')['data'][0]
  # print(feed_id)

  # fb_like_status = graph.put_object(parent_object=comment_id, connection_name='likes')


  # for idx in range(0, 20):
    # comment = graph.get_object(page_id+'/feed')['data'][idx]
#     comment_id = comment['id']
#     fb_like_status = graph.put_object(parent_object=comment_id, connection_name='likes')
#     print('No.%s | %s | (name = %s id = %s) | comment_id = %s | like_status = %s' %(numbers, current_time(), page_name, page_id, comment_id, fb_like_status))
#     rand_sleep_time(2, 6)
#     print('===========================================================================\n')
#     numbers += 1

#   rand_sleep_time(10, 17)

# search_list = get_fb_search_result_list(graph, '心情', "page")
# dump_fb_search_list(search_list[:20])

# comment = graph.get_object('417506414983829/feed')
# comment_id = comment['data'][0]['id']
# print(comment_id)


# message = '謝謝分享，感恩'
# fb_post_id = graph.put_object(parent_object=comment_id, connection_name='comments', message = message)
