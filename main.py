import json
import time
from random import randrange

import telebot
from telebot import types

import config

bot = telebot.TeleBot(config.token)


def keyToSortWords(word):
    try:
        return word['right']/word['all']
    except ZeroDivisionError:
        return randrange(-100, 0)


def readDB():
    dataBase = {}
    try:
        file = open(config.dbFileName, encoding='UTF-8')
    except FileNotFoundError:
        file = open(config.dbFileName, 'w')
        file.write(json.dumps(dataBase))
        file.close()
    else:
        dataBase = json.loads(file.read())
        file.close()
    return dataBase


def writeDB(dataBase):
    with open(config.dbFileName, 'w', encoding='UTF-8') as file:
        file.write(
            json.dumps(
                dataBase,
                indent=4,
                sort_keys=True
            )
        )
        file.close()


dataBase = readDB()

udarsFile = open(config.udarsFileName, encoding='UTF-8')
udarsJson = udarsFile.read()
udars = json.loads(udarsJson)
numOfWords = len(udars)
whichWordChoosen = {}


@bot.message_handler()
def sendWord(message):
    user = message.chat.id

    try:
        words = dataBase[str(user)]
    except KeyError:
        words = [{'right': 0, 'all': 0, 'index': i} for i in range(numOfWords)]

    words.sort(key=keyToSortWords)

    markup = types.ReplyKeyboardMarkup()
    for possible in udars[words[0]['index']]['all']:
        markup.row(possible)
    
    bot.send_message(
        message.chat.id,
        udars[words[0]['index']]['correct'].lower(),
        reply_markup=markup
    )
    bot.register_next_step_handler(message, checkAnswer)

    whichWordChoosen[message.chat.id] = words[0]
    words[0]['all'] += 1
    dataBase[str(user)] = words
    writeDB(dataBase)


def checkAnswer(message):
    text = message.text
    user = message.chat.id
    wordChoosen = whichWordChoosen[message.chat.id]

    if text == udars[wordChoosen['index']]['correct']:
        bot.send_message(
            message.chat.id,
            'Верно!',
        )

        for word in dataBase[str(user)]:
            if word['index'] == wordChoosen['index']:
                word['right'] += 1
                print(word)
                break

        writeDB(dataBase)
        sendWord(message)
    else:

        bot.send_message(
            message.chat.id,
            f'Правильно будет - {udars[wordChoosen["index"]]["correct"]}!',
        )
        sendWord(message)


while True:
    try:
        bot.polling()
    except Exception as e:
        print(e)
        raise KeyboardInterrupt
        bot.stop_polling()
        time.sleep(5)
