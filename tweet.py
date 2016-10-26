import tweepy, random, urllib, json, datetime, time, os
import settings, auth

def main():
    while(1):
        #check if between 13:00 and 13:10
        now = datetime.datetime.now()
        if(now.hour != 13 or now.minute >= 10):
            time.sleep(60 * 10)
            continue

        #in valid time, compose tweet
        api = getAPI()

        #find file
        day = time.strftime("%m-%d-%y")
        for i in range(0, 13):
            if(i == 12):
                filename = "" #no file on the 12 hour found, just skip today
                break
            filename = "../MTU-Timelapse/cam/%s/12-%s.jpg" % (day, str(i * 5).zfill(2))
            if(os.path.isfile(filename)):
                break

        if(filename == ""):
            continue

        #post tweet
        degrees, weather = getWeather()
        fileurl = "http://joshjohnson.io/" + filename.replace("../", "")
        tweet = settings.TWEET % (random.choice(settings.TWEETINTRO), degrees, weather, fileurl)
        #api.update_with_media(filename, status=tweet)
        print tweet

        time.sleep(60 * 10)

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
