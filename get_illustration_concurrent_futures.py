from requests_oauthlib import OAuth1Session
import concurrent.futures
import json
import os
import urllib
import setting

import datetime
import time
import calendar

PYTHONASYNCIODEBUG  =1
twitter = OAuth1Session(setting.CONSUMER_KEY, setting.CONSUMER_SECRET, setting.ACCESS_TOKEN, setting.ACCESS_TOKEN_SECRET)

# 検索対象のuser id名を指定
screen_name= "maoutokagura"

#保存するフォルダ名
mkdir_name = "twitter_get_image/" + screen_name
#合計のgetするtweetの数は (get_count -1) × get_times
#一度にgetするtweetの数。最大200
get_count = 200
#何回tweetをgetするか
get_times = 20
#リツイートを含めるか。0含めない。1含める。
include_rts= 1

executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

#http://blog.unfindable.net/archives/4302
def YmdHMS(created_at):
    time_utc = time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
    unix_time = calendar.timegm(time_utc)
    time_local = time.localtime(unix_time)
    return str(time.strftime("%Y-%m-%d %H:%M:%S", time_local))

def dir_check():
    if not os.path.isdir(mkdir_name):
#        os.mkdir(mkdir_name)
        os.makedirs(mkdir_name)
    check_count = 0
    while True:
        if not os.path.isdir(mkdir_name + "/dir" + str(check_count)):
            os.mkdir(mkdir_name + "/dir" + str(check_count))
            dir_name = "/dir" + str(check_count)
            return dir_name
        check_count += 1

def get_tweet_in_json(max_id = None):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    params = {'screen_name':screen_name,
        'count':get_count,
        'include_rts':include_rts
          }
    if max_id is not None:
        params['max_id'] = max_id
    req = twitter.get(url, params = params)
    timeline = json.loads(req.text)
    return timeline

def get_target_timeline():
    timeline = get_tweet_in_json()
    temp_id = timeline[-1]['id']
    for i in range(get_times):
        temp_timeline = get_tweet_in_json(temp_id)
        temp_timeline.pop(0)
        timeline = timeline + temp_timeline
        if len(temp_timeline)  < 1:
            break
        temp_id = temp_timeline[-1]['id']
    i=0
    for tweet in timeline:
        print( str(i) +'  '+ str(tweet['id']) + '  ' + (str(tweet['created_at'])) + '  ' + str(YmdHMS(tweet['created_at'])))
        i+=1
    return timeline

def get_image_data(filename,temp_image):
    print(filename)
    print(temp_image)
    with open(filename, 'wb') as f:
        img = urllib.request.urlopen(temp_image).read()
        f.write(img)


def get_illustration(timeline,dir_name):
    image_number = 0
    check_image = []
    for tweet in timeline:
        try:
            media_list = tweet['extended_entities']['media']
            for media in media_list:
                image = media['media_url']
                if image in check_image:
                    continue
                filename = mkdir_name + dir_name +"/"+str(image_number).zfill(4) +"_"+YmdHMS(tweet['created_at'])+"_"+os.path.basename(image)
                executor.submit(get_image_data,filename,image)
                check_image.append(image)
                image_number += 1
            print(str(tweet['id']) + '  ' + YmdHMS(tweet['created_at']) + '  ' + "get tweet media")
        except KeyError:
            print(str(tweet['id']) + '  ' + YmdHMS(tweet['created_at']) + '  ' + "KeyError:画像を含んでいないツイートです")
        except:
            print("error")


if __name__ == '__main__':
    dir_name = dir_check()
    all_list = []
    timeline = get_target_timeline()
    get_illustration(timeline, dir_name)
