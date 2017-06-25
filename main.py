import urllib
import requests
from key import ACCESS_TOKEN
BASE_URL="https://api.instagram.com/v1"
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import matplotlib.pyplot as plt


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
        print "The id of the user is "+str(search_results['data'][0]['id'])
        return search_results['data'][0]['id']

#if search not succesful
    else:
      print 'User does not exist!'
  else:
    print 'Status code other than 200 was received!'



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
    else:
      print "There is no recent post!"
  else:
    print "Status code other than 200 received!"

    return get_user_id()

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
  request_url = (BASE_URL + '/users/%s/media/recent/?access_token=%s') % (user_id, ACCESS_TOKEN)
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


#like a post

def like_a_post(insta_username):
  media_id = get_post_id(insta_username)
  request_url = (BASE_URL + '/media/%s/likes') % (media_id)
  print 'Liking the post: %s' % (request_url)
  payload = {"access_token": ACCESS_TOKEN}

  post_a_like = requests.post(request_url, payload).json()
  if post_a_like['meta']['code'] == 200:
    print 'Like was successful!'
  else:
    print 'Your like was unsuccessful. Try again!'

#get comment list

def get_comment_list(insta_username):
  media_id = get_post_id(insta_username)
  request_url = (BASE_URL + '/media/%s/comments?access_token=%s') % (media_id, ACCESS_TOKEN)
  comment_info = requests.get(request_url).json()
  if comment_info['meta']['code'] == 200:
    if len(comment_info['data']):
      for x in range(0, len(comment_info['data'])):
        print 'Comment: %s || User: %s' % (comment_info['data'][x]['text'], comment_info['data'][x]['from']['username'])
    else:
        print 'There are no comments on this post!'
  else:
      print 'Status code other than 200 received!'


#post a comment
def make_a_comment(insta_username):
  media_id = get_post_id(insta_username)
  comment_text = raw_input("Your comment: ")
  payload = {"access_token": ACCESS_TOKEN, "text" : comment_text}

  request_url = (BASE_URL + '/media/%s/comments') % (media_id)
  print 'Making comment on post: %s' % (request_url)
  make_comment = requests.post(request_url, payload).json()
  if make_comment['meta']['code'] == 200:
    print "Successfully added a new comment!"
  else:
    print "Unable to add comment. Try again!"

def delete_negative_comment(insta_username):
  media_id = get_post_id(insta_username)
  request_url = (BASE_URL + '/media/%s/comments/?access_token=%s') % (media_id, ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  comment_info = requests.get(request_url).json()

  if comment_info['meta']['code'] == 200:
      if len(comment_info['data']):
          # Here's a naive implementation of how to delete the negative comments :)
          for x in range(0, len(comment_info['data'])):
              comment_id = comment_info['data'][x]['id']
              comment_text = comment_info['data'][x]['text']
              blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
              if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                  print 'Negative comment : %s' % (comment_text)
                  delete_url = (BASE_URL + '/media/%s/comments/%s/?access_token=%s') % (
                  media_id, comment_id, ACCESS_TOKEN)
                  print 'DELETE request url : %s' % (delete_url)
                  delete_info = requests.delete(delete_url).json()

                  if delete_info['meta']['code'] == 200:
                      print 'Comment successfully deleted!\n'
                  else:
                      print 'Unable to delete comment!'
              else:
                  print 'Positive comment : %s\n' % (comment_text)
      else:
          print 'There are no existing comments on the post!'
  else:
      print 'Status code other than 200 received!'

def compare(insta_username):
    neg_count=0
    pos_count=0
    media_id = get_post_id(insta_username)

    request_url = (BASE_URL + '/media/%s/comments/?access_token=%s') % (media_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    neg_count = neg_count +1
                    print "Negative comment:"
                    print str(neg_count)
                else:
                    pos_count = pos_count + 1
                    print" Positive comment:"
                    print str(pos_count)

    labels = ['Negative comments', 'Positive  comments']
    sizes = [neg_count , pos_count]
    colors = ['yellowgreen', 'gold']
    plt.pie(sizes, colors=colors, shadow=True,labels=labels,startangle=90)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

'''def hashtag_analysis(insta_username):

    user_id = get_user_id(insta_username)
    request_url = (BASE_URL + '/users/%s/media/recent/?access_token=%s') % (user_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    hashtag_info = requests.get(request_url).json()

    if hashtag_info['meta']['code'] == 200:
        if len(hashtag_info['data']):
            for x in range(0, len(hashtag_info['data'])):
                hash_text = hashtag_info['data'][x]['id']['tags']
                dict={ hashtag_info :

                }
        else:
            print 'There are no tags on this post!'
    else:
        print 'Status code other than 200 received!'
'''

def start_bot():
    while True:
        print '\n'
        print 'WELCOME to InstaBot!'
        print ' Menu options. Please choose:'
        print "1.Get your own details"
        print "2.Get details of a user by username"
        print "3.Get your own recent post"
        print "4.Get the recent post of a user by username "
        print "5.Get users ID"
        print "6.Get a list of people who have liked the recent post of a user"
        print "7.Like the recent post of a user"
        print "8.Get a list of comments on the recent post of a user"
        print "9.Make a comment on the recent post of a user"
        print "10.Delete negative comments from the recent post of a user"
        print "11.Compare as positive and negative comments  "
        print "12.Exit"



        choice = raw_input("Enter you choice: ")
        if choice == "1":
            self_info()
        elif choice == "2":
            insta_username = raw_input("Enter the username of the user: ")
            user_info(insta_username)
        elif choice == "3":
            get_own_post()
        elif choice == "4":
            insta_username = raw_input("Enter the username of the user: ")
            get_users_post(insta_username)
        elif choice == "5":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_id(insta_username)
        elif choice=="6":
           insta_username = raw_input("Enter the username of the user: ")
           get_like_list(insta_username)
        elif choice=="7":
           insta_username = raw_input("Enter the username of the user: ")
           like_a_post(insta_username)
        elif choice=="8":
           insta_username = raw_input("Enter the username of the user: ")
           get_comment_list(insta_username)
        elif choice=="9":
           insta_username = raw_input("Enter the username of the user: ")
           make_a_comment(insta_username)
        elif choice=="10":
           insta_username = raw_input("Enter the username of the user: ")
           delete_negative_comment(insta_username)
        elif choice == "11":
            insta_username = raw_input("Enter the username of the user: ")
            compare(insta_username)
        elif choice == "12":
            exit()
        else:

            print "wrong choice"

start_bot()