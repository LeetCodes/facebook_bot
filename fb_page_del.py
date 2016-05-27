from facebot import Facebook

import facebook
import fbconsole
import requests
import json
import time
from datetime import datetime, date, timedelta



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
  page_token = accounts['data'][0]['access_token']
  return page_token

def get_fb_page_graph_instance(username, password):
  page_token = get_fb_page_token(username, password)
  page_graph = facebook.GraphAPI(page_token)
  return page_graph

def current_time():
  return '[' + (datetime.now()).strftime('%Y/%m/%d %H:%M:%S') + ']'



username = 'tittan0829@gmail.com'
password = 'Novia0829'
art_start_no = 3210
art_end_no   = 3425

page_token = get_fb_page_token(username, password)
page_graph = facebook.GraphAPI(page_token)
dobee01_id = '1020239824709036'

feed_datas = page_graph.get_object(dobee01_id+'/feed')

for each_feed in fbconsole.iter_pages(feed_datas):
  feed_id = each_feed['id']
  print(feed_id)
  page_graph.delete_object(id=feed_id)

