import tweepy, random
import settings, auth

def main():
    api = getAPI()
    filename = "../MTU-Timelapse/cam/10-25-16/12-00.jpg"
    tweet = settings.TWEET % (random.choice(settings.TWEETINTRO), 65, "cloudy")
    api.update_with_media(filename, status=tweet)
    print "Posted tweet '%s' with image '%s'" % (tweet, filename)


def getAPI():
    authorization = tweepy.OAuthHandler(auth.CKEY, auth.CSECRET)
    authorization.set_access_token(auth.AKEY, auth.ASECRET)
    api = tweepy.API(authorization)
    return api


if __name__ == "__main__":
    main()
