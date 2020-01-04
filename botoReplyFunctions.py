import words
import random
import time
import requests
import keys
import json

swearCounter = -1
noUnderstandCounter = -1
userName = ''


def randomNum(listToRandom):
    return random.randint(0, len(listToRandom) - 1)


def removeUselessWords(user_message):
    querywords = user_message.split()
    newQuery = []
    for word in querywords:
        if word not in words.wordsToRemove:
            newQuery.append(word)

    newQuery = ' '.join(newQuery)
    return newQuery


def cleanString(user_message):
    querywords = user_message.split()
    newQuery = []
    for word in querywords:
        if word not in words.wordsToRemove and word not in words.questions:
            word = word[:-1] if word.endswith('?') else word
            newQuery.append(word)
    newQuery = ' '.join(newQuery)
    return newQuery


def getJoke():
    joke = requests.get('http://api.icndb.com/jokes/random/')
    joke = joke.json()
    return joke['value']['joke'] + '   ha ha ha, this api is so funny!'


def searchWiki(user_message):
    toList = user_message.split(' ')
    toQuery = '_'.join(toList)
    response = requests.get(
        'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles=' + toQuery)
    responseJson = response.json()
    key = responseJson['query']['pages'].keys()
    key = list(key)
    if key[0] == '-1':
        return 'Sorry could not find this in wikipedia'
    else:
        article = responseJson['query']['pages'][key[0]]['extract']
        # print(responseJson['query']['pages'][key[0]]['extract'])
        index = article.find('.')
        article = article[:index+1]
        # print(article)
        return article


def handleQuestions(user_message):
    if 'your dog' in user_message or 'i ' in user_message:
        return 'the name of my dog is "bobo"', 'dog'
    if 'you' in user_message:
        return talkingAboutBoto(user_message), 'excited'
    if 'me' in user_message or 'i ' in user_message:
        return talkingAboutUser(user_message), 'inlove'
    if 'weather' in user_message:
        return getWeather(cleanString(user_message))
    else:
        return searchWiki(cleanString(user_message)), 'takeoff'


def talkingAboutUser(user_message):
    return 'talking about user'


def talkingAboutBoto(user_message):
    if 'who' in user_message:
        return "My name is boto, i'm here to help"
    if 'what' in user_message:
        return "I'm just a bot actually"


def getWeather(user_message):
    #user_message = removeUselessWords(user_message)

    api_key = keys.weatherMapApiKey
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = user_message
    complete_url = base_url + "appid=" + api_key + \
        "&q=" + city_name + '&units=metric'
    response = requests.get(complete_url)
    responseJson = response.json()

    if responseJson["cod"] != "404":
        y = responseJson["main"]
        current_temperature = y["temp"]
        current_humidiy = y["humidity"]
        return 'The weather in ' + user_message + ' is: ' + str(current_temperature) + '° celsius and humidity is ' + str(current_humidiy) + '%', 'inlove'

    else:
        return 'Sorry city Not Found. The sintax should be like: "what is the weather in tel aviv"', 'crying'


def checkAnswer(user_message):
    global userName
    global swearCounter
    global noUnderstandCounter

    stringAfterCleaning = removeUselessWords(user_message)
    ######################boto do handeling swear words ###########################

    if swearCounter == 2:
        return 'boto is mad at you, and not talking to you any more!', 'crying'
    if any(word in words.user_swear for word in user_message.split(' ')):
        swearCounter += 1
        return (userName + ' ' + words.boto_angry[swearCounter]), 'no'
    ######################boto reply to greetings ###########################
    if not userName:
        userName = stringAfterCleaning
        return 'nice to meet you ' + stringAfterCleaning + ' what do you want to ask me?', 'excited'

    if any(word in words.user_greet for word in user_message.split(' ')):
        return words.boto_greet[randomNum(words.boto_greet)], 'excited'

    ######################boto tells a joke ###########################

    if 'joke' in user_message:
        return getJoke(), 'giggling'
    ######################boto python ###########################
    if 'python' in user_message or 'i ' in user_message:
        return "i'm afraid of snakes", 'afraid'
    ######################boto handels questions ###########################

    if user_message.endswith('?') or any(word in words.questions for word in user_message.split(' ')):
        return handleQuestions(user_message)

    ######################boto do not anderstand ###########################
    else:
        if noUnderstandCounter == 2:
            noUnderstandCounter = -1
        else:
            noUnderstandCounter += 1
        return words.boto_notUnderstand[noUnderstandCounter], 'confused'
