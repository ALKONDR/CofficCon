# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import telegram
import requests
import json

LAST_UPDATE_ID = None
bot_token = '157862321:AAFo0b8B8hlcYTEvPhMN99NQ-CsJl5ATXQw'
bot_phrases = []
commands = []
choose_van = [[ '1' , '2' , '3' ]]
choose_van_keyboard = telegram.ReplyKeyboardMarkup(choose_van, one_time_keyboard = True)
choose_coffee = [[ '1' , '2' , '3' , '4' , '5' ], [ '6' , '7' , '8' , '9' , '10' ]]
choose_coffee_keyboard = telegram.ReplyKeyboardMarkup(choose_coffee, one_time_keyboard = True)
choose_size = [[ '0.3' , '0.5' ]]
choose_size_keyboard = telegram.ReplyKeyboardMarkup(choose_size, one_time_keyboard = True)
more_cancel = [[ 'More' , 'Get bill' ]]
more_cancel_keyboard = telegram.ReplyKeyboardMarkup(more_cancel, one_time_keyboard = True)
coffee_base = {}
order = None
order_in_process = False
choosing_coffee = False
choosing_size = False
choosing_more_cancel = False
coffee_list = []
cur_coffee = None
choosing_location = False
choosing_van = False
full_sum = 0

class Order(object):

    def __init__(self):
        self.van = None
        self.coffee = {}
        self.price = 0

    def get_price(self):
        return self.price

    def add_coffee(self, coffee, size):
        self.coffee[ {coffee : size} ] = self.coffee.get( {coffee : size}, 0) + 1
        self.sum += coffee_base[size][coffee]

    def delete_coffee(self, coffee, size, amount):
        if not {coffee : size} in self.coffee or self.coffee[ {coffee : size} ] < count:
            bot = telegram.Bot(token = bot_token)
            bot.sendMessage(chat_id = chat_id, text = bot_phrases[5])
            return
        self.price -= coffee_base[coffee][size] * amount
        self.coffee[ {coffee : size} ] -= amount

    def is_correct(self):
        if len(self.coffee) != 0 and self.van != None:
            return True
        return False


def main():
    inp_phrase = open('phrases.txt', 'r')
    for line in inp_phrase:
        # line = line.encode('utf-8')
        bot_phrases.append(line)

    inp_coffee = open('coffee_base.txt', 'r')
    for line in inp_coffee:
        # tmp_cof = line.decode('utf-8')
        tmp_cof = line.split()
        coffee_base[ tmp_cof[0] ] = { '0.3' : int(tmp_cof[1]) , '0.5' : int(tmp_cof[2]) }
        coffee_list.append(tmp_cof[0])

    inp_commands = open('commands.txt', 'r')
    for line in inp_commands:
        commands.append(line)

    print bot_phrases
    print commands
    print coffee_base
    print coffee_list

    bot = telegram.Bot(token = bot_token)
    try:
        LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
    except IndexError:
        LAST_UPDATE_ID = None

    while(True):
        echo(bot)

def echo(bot):
    global LAST_UPDATE_ID
    global order
    global order_in_process
    global choosing_coffee
    global choosing_size
    global choosing_more_cancel
    global coffee_list
    global cur_coffee
    global choosing_location
    global choosing_van
    global choose_sum
    global full_sum

    for update in bot.getUpdates(offset = LAST_UPDATE_ID, timeout = 50):
        chat_id = update.message.chat_id
        message = None
        try:
            message = update.message.text.encode('utf-8')
        except:
            pass

        if message == commands[0]:
            # order = Order()
            order_in_process = True
            choosing_coffee = True
            text = ""
            i = 0
            for key in coffee_base:
                text += "%s. %s:\n 0,3%s: %s%s 0,5%s: %s%s\n" % (str(i + 1), key, bot_phrases[8], str(coffee_base[key]['0.3']), bot_phrases[7], bot_phrases[8], str(coffee_base[key]['0.5']), bot_phrases[7])
                i += 1
            bot.sendMessage(chat_id = chat_id, text = text, reply_markup = choose_coffee_keyboard)
        elif order_in_process and choosing_coffee:
            if message:
                cur_coffee = coffee_list[int(message) - 1]
            # print coffee_list, int(message)
            # print coffee_list[int(message) - 1]
            choosing_coffee = False
            choosing_size = True
            bot.sendMessage(chat_id = chat_id, text = bot_phrases[10], reply_markup = choose_size_keyboard)
            print type(message), message
        elif order_in_process and choosing_size:
            # order.add_coffee(cur_coffee, message)
            # print cur_coffee, message
            if cur_coffee:
                full_sum += int(coffee_base[cur_coffee][message])
            cur_coffee = None
            choosing_size = False
            choosing_more_cancel = True
            bot.sendMessage(chat_id = chat_id, text = bot_phrases[11], reply_markup = more_cancel_keyboard)
        elif order_in_process and choosing_more_cancel:
            choosing_more_cancel = False
            if (message == 'Get bill'):
                choosing_coffee = False
                order_in_process = False
                bot.sendMessage(chat_id = chat_id, text = bot_phrases[12] + str(full_sum) + " " + bot_phrases[7], reply_markup = choose_coffee_keyboard)
                bot.sendMessage(chat_id = chat_id, text = bot_phrases[13])
                bot.sendMessage(chat_id = chat_id, text = bot_phrases[9])
                order = None
                choosing_location = True
            else:
                text = ""
                i = 0
                for key in coffee_base:
                    text += "%s. %s:\n 0.3%s: %s%s 0.5%s: %s%s\n" % (str(i + 1), key, bot_phrases[8], str(coffee_base[key]['0.3']), bot_phrases[7], bot_phrases[8], str(coffee_base[key]['0.5']), bot_phrases[7])
                    i += 1
                bot.sendMessage(chat_id = chat_id, text = text, reply_markup = choose_coffee_keyboard)
                choosing_coffee = True
        elif choosing_location:
            print "we choose location"
            loc = None
            lat = None
            lon = None
            try:
                loc = update.message.location
                print loc
                lat = float(loc.latitude)
                print lat
                lon = float(loc.longitude)
                print lon
            except:
                pass

            #TODO: have to get these points from our database
            vans = [(37.127150, 55.324397), (37.144839, 55.306868), (37.153630, 55.318577)]

            if loc:
                print "yandex api"
                map = 'https://static-maps.yandex.ru/1.x/?size=450,450&l=sat,skl&z=13&ll=%s,%s&pt=%s,%s,comma' % (str(lon), str(lat), str(lon), str(lat))

                for i in range(len(vans)):
                    map += ('~%s,%s,pmwtm%s' % (str(vans[i][0]), str(vans[i][1]), str(i + 1)))
                print map

                bot.sendPhoto(chat_id = chat_id, photo = map)
                print 'dont fall here'
                bot.sendMessage(chat_id = chat_id, text = bot_phrases[0], reply_markup = choose_van_keyboard)
                choosing_van = True
        elif choosing_van:
            bot.sendMessage(chat_id = chat_id, text = bot_phrases[14])

        LAST_UPDATE_ID = update.update_id + 1


main()
