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
art_start_no = 10300
art_end_no   = 10370

page_token = get_fb_page_token(username, password)
page_graph = facebook.GraphAPI(page_token)
dobee01_id = '1020239824709036'

for post_id in range(art_start_no, art_end_no):
  expired_time = get_access_token_expired_time(page_token)
  if (expired_time < (60 * 11)):
    print('Page Token is expired, prepare to reget page token\n')
    page_graph = get_fb_page_graph_instance(username, password)

  art_link = 'http://www.dobee01.com/p/{}/'.format(post_id)
  try:
    post_id = page_graph.put_object(parent_object=dobee01_id, connection_name='feed', link=art_link)
    print(current_time(), art_link, 'has been publish to dobee01 page, prepare sleep 300 seconds, post_id = ', post_id)
    time.sleep(600)
  except:
    print(current_time(), art_link, 'has somthing wrong to publish dobee01 facebook page\n')
    time.sleep(5)
    pass









