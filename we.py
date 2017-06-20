
#

    else:
      print "There is no recent post!"
  else:
    print "Status code other than 200 received!"

  return None


#get users post
def get_users_post(insta_username):
  user_id = get_user_id(insta_username)
  request_url = (BASE_URL + '/users/%s/media/recent?access_token=%s') % (user_id, ACCESS_TOKEN)
  print 'Requesting media for: %s' % (request_url)
  recent_post = requests.get(request_url).json()
  if recent_post['meta']['code'] == 200:
    if len(recent_post['data']):
      image_name = recent_post['data'][0]['id'] + ".jpeg"
      image_url = recent_post['data'][0]['images']['standard_resolution']['url']
      urllib.urlretrieve(image_url, image_name)

    else:
      print "There is no recent post!"
  else:
    print "Status code other than 200 received!"

  return None

#get post id

def get_post_id(insta_username):
  user_id = get_user_id(insta_username)
  request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, ACCESS_TOKEN)
  print 'Requesting data for : %s' % (request_url)
  user_media = requests.get(request_url).json()

  if user_media['meta']['code'] == 200:
    if len(user_media['data']):
      return user_media['data'][0]['id']
    else:
      print 'Post does not exist!'
  else:
    print 'Status code other than 200 received!'
  return None


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