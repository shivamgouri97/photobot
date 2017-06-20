








#get liked list
def get_like_list(insta_username):
  post_id = get_post_id(insta_username)

  request_url = (BASE_URL + '/media/%s/likes?access_token=%s') % (post_id, ACCESS_TOKEN)
  likes_info = requests.get(request_url).json()
  if likes_info['meta']['code'] == 200:
    if len(likes_info['data']):
      for x in range(0, len(likes_info['data'])):
        print likes_info['data'][x]['username']
    else:
      print 'No user has liked the post yet!'
  else:
      print 'Status code other than 200 received!'