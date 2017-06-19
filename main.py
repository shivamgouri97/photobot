import requests
from key import ACCESS_TOKEN
BASE_URL="http://api.instagram.com/v1"
def self_info():
  request_url = (BASE_URL + '/users/self/?access_token=%s') % (ACCESS_TOKEN)
  print 'Requesting info for:' + request_url
  my_info = requests.get(request_url).json()
  print 'My info is:\n', my_info
  print 'My Followers: %s\n' % (my_info['data']['counts']['followed_by'])
  print 'People I Follow: %s\n' % (my_info['data']['counts']['follows'])
  print 'No. of posts: %s\n' % (my_info['data']['counts']['media'])

#getting self information
self_info()

#getting user id by username
def get_user_id(insta_username):
  request_url = (BASE_URL + '/users/search?q=%s&access_token=%s') % (insta_username, ACCESS_TOKEN)
  print'Requesting info for:' + request_url

  search_results = requests.get(request_url).json()

  if search_results['meta']['code'] == 200:
    if len(search_results['data']):
      return search_results['data'][0]['id']
    else:
      print 'User does not exist!'
  else:
    print 'Status code other than 200 was received!'

  return None

