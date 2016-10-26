import tweepy, random, urllib, json, datetime, time, os
import settings, auth
from PIL import Image

def main():
    #sunrise, noon, sunset
    posted = [0, 0, 0]
    while(1):
        #reset posted
        now = datetime.datetime.now()
        if(now.hour == 0):
            posted = [0, 0, 0]

        #in valid time, compose tweet
        #api = getAPI()

        if(now.hour >= 4 and now.hour < 10 and not posted[0]):
            found, filename = check("sunrise")
            if(found):
                post("sunrise", filename)
                posted[0] = 1

        if(now.hour == 12 and not posted[1]):
            found, filename = check("noon")
            if(found):
                post("noon", filename)
                posted[1] = 1

        if(now.hour >= 16 and now.hour < 23 and not posted[2]):
            found, filename = check("sunset")
            if(found):
                post("sunset", filename)
                posted[2] = 1

        time.sleep(60 * 5)

def check(event):
    now = datetime.datetime.now()
    curMinute = now.minute - now.minute % 5
    curHour = now.hour

    #noon
    if(event == "noon"):
        #check last image
        filename = "../MTU-Timelapse/cam/%s-%s-%s/%s-%s.jpg" % (str(now.month).zfill(2), str(now.day).zfill(2), str(now.year)[-2:], str(curHour).zfill(2), str(curMinute).zfill(2))
        if(not os.path.isfile(filename)):
            return 0, ""
        else:
            return 1, filename

    #sunrise, sunset
    else:
        #check last 10 images
        for i in range(9, -1, -1):
            m = curMinute - (5 * i)
            h = curHour
            if(m < 0):
                m += 60
                h -= 1

            filename = "../MTU-Timelapse/cam/%s-%s-%s/%s-%s.jpg" % (str(now.month).zfill(2), str(25).zfill(2), str(now.year)[-2:], str(h).zfill(2), str(m).zfill(2))
            if(not os.path.isfile(filename)):
                continue

            #check color
            ave = getAverageRGB(filename)
            if(event == "sunrise" and ave >= settings.SUNRISETHRESHOLD or event == "sunset" and ave < settings.SUNSETTHRESHOLD):
                return 1, filename

    return 0, ""

def post(event, filename):
    api = getAPI()
    #post tweet
    degrees, weather = getWeather()
    weather = "%s%s" % ("" if weather.endswith("s") else "a ", weather)
    fileurl = "http://joshjohnson.io/" + filename.replace("../", "")

    if(event == "sunrise"):
        intros = settings.RISEINTRO
    elif(event == "noon"):
        intros = settings.NOONINTRO
    elif(event == "sunset"):
        intros = settings.SETINTRO

    tweet = settings.TWEET % (random.choice(intros), degrees, weather, fileurl)
    #api.update_with_media(filename, status=tweet)
    print tweet


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

def getAverageRGB(file):
    rgb = 0
    count = 0
    newsize = 640, 360
    image = Image.open(file)
    image.thumbnail(newsize, Image.ANTIALIAS)
    for channel in range(3):
        pixels = image.getdata(band=channel)

        for pixel in pixels:
            rgb += pixel
            count += 1

    return rgb / count

if __name__ == "__main__":
    main()
