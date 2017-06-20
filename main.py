import urllib
import requests
from key import ACCESS_TOKEN
BASE_URL="http://api.instagram.com/v1"

#function to get self info
def self_info():
  request_url = (BASE_URL + '/users/self/?access_token=%s') % (ACCESS_TOKEN)
  print 'Requesting info for:' + request_url
  my_info = requests.get(request_url).json()
  print 'My info is:\n', my_info
  print 'My Followers: %s\n' % (my_info['data']['counts']['followed_by'])
  print 'People I Follow: %s\n' % (my_info['data']['counts']['follows'])
  print 'No. of posts: %s\n' % (my_info['data']['counts']['media'])



#getting user id by username
def get_user_id(insta_username):
  request_url = (BASE_URL + '/users/search?q=%s&access_token=%s') % (insta_username, ACCESS_TOKEN)
  print'Requesting info for:' + request_url

  search_results = requests.get(request_url).json()
# if search successful
  if search_results['meta']['code'] == 200:
    if len(search_results['data']):
      return search_results['data'][0]['id']
#if search not succesful
    else:
      print 'User does not exist!'
  else:
    print 'Status code other than 200 was received!'
    exit()


# getting user info by using user id'''
def user_info(insta_username):
  user_id = get_user_id(insta_username)
  request_url = (BASE_URL + '/users/%s/?access_token=%s') % (user_id, ACCESS_TOKEN)
  print 'Requesting info for:' + request_url
  user_info = requests.get(request_url).json()

  print '%s info is:\n' % (insta_username)
  print user_info
  print '%s Followers: %s\n' % (insta_username, user_info['data']['counts']['followed_by'])
  print 'People %s Follow: %s\n' % (insta_username, user_info['data']['counts']['follows'])
  print 'No. of posts: %s\n' % (user_info['data']['counts']['media'])

#get own posts
def get_own_post():
  request_url = (BASE_URL + '/users/self/media/recent?access_token=%s') % (ACCESS_TOKEN)
  print 'Requesting media for: %s' % (request_url)

  recent_post = requests.get(request_url).json()
  if recent_post['meta']['code'] == 200:
    if len(recent_post['data']):
      #download image
      image_name = recent_post['data'][0]['id'] + ".jpeg"
      image_url = recent_post['data'][0]['images']['standard_resolution']['url']
      urllib.urlretrieve(image_url, image_name)