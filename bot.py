import telegram
import requests
import json

LAST_UPDATE_ID = None
bot_phrases = []

def main():
    inp = open('phrases.txt', 'r')
    for line in inp:
        bot_phrases.append(line.decode('utf-8'))

    bot = telegram.Bot(token = '157862321:AAFo0b8B8hlcYTEvPhMN99NQ-CsJl5ATXQw')
    try:
        LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
    except IndexError:
        LAST_UPDATE_ID = None

    while(True):
        echo(bot)

def echo(bot):
    global LAST_UPDATE_ID
    for update in bot.getUpdates(offset = LAST_UPDATE_ID, timeout = 10):
        chat_id = update.message.chat_id
        message = None
        print update.message
        try:
            message = update.message.text.encode('utf-8')
        except:
            pass

        loc = None
        lat = None
        lon = None
        try:
            loc = update.message.location
            lat = float(loc.latitude)
            lon = float(loc.longitude)
        except:
            pass

        #TODO: have to get these points from our database
        vans = [(37.127150, 55.324397), (37.144839, 55.306868), (37.153630, 55.318577)]

        if loc:
            print lat, lon
            map = 'https://static-maps.yandex.ru/1.x/?size=450,450&l=sat,skl&z=13&ll=%s,%s&pt=%s,%s,comma' % (str(lon), str(lat), str(lon), str(lat))

            for i in range(len(vans)):
                map += ('~%s,%s,pmwtm%s' % (str(vans[i][0]), str(vans[i][1]), str(i + 1)))
            print map

            bot.sendPhoto(chat_id = chat_id, photo = map)
            bot.sendMessage(chat_id = chat_id, text = bot_phrases[0])



        LAST_UPDATE_ID = update.update_id + 1

main()