"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json


list_swear = ["fuck", "shit", "motherfucker", "bitch", "slut", "whore"]


@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    bot_output = parsing(user_message)
    return json.dumps(bot_output)


def parsing(user_message):
    user_split_message = user_message.split(" ")

    for word in user_split_message:
        if word in list_swear:
            bot_response = "Please don't swear at me!"
            animation = "inlove"
            print(bot_response)
            return {"animation": animation, "msg": bot_response}
    return {"animation": "inlove", "msg": "nothing to say dude"}




@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)


if __name__ == '__main__':
    main()
