import tweepy, random, urllib, json, time, os
import settings, auth

def main():
    api = getAPI()

    day = time.strftime("%m-%d-%y")

    for i in range(0, 13):
        filename = "../MTU-Timelapse/cam/%s/12-%s.jpg" % (day, str(i * 5).zfill(2))
        if(os.path.isfile(filename)):
            break

    degrees, weather = getWeather()
    tweet = settings.TWEET % (random.choice(settings.TWEETINTRO), degrees, weather)
    #api.update_with_media(filename, status=tweet)
    print "Posted tweet '%s' with image '%s'" % (tweet, filename)


def getAPI():
    authorization = tweepy.OAuthHandler(auth.CKEY, auth.CSECRET)
    authorization.set_access_token(auth.AKEY, auth.ASECRET)
    api = tweepy.API(authorization)
    return api

def getWeather():
    url = "http://api.openweathermap.org/data/2.5/weather?q=Houghton&APPID=" + auth.WEATHERKEY
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    kelvin = data['main']['temp']
    degrees = kelvin * 9/5 - 459.67
    weather = data['weather'][0]['description']
    return degrees, weather

if __name__ == "__main__":
    main()
