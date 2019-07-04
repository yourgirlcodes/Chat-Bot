"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
import random


list_swear = ["fuck", "shit", "motherfucker", "bitch", "slut", "whore", "idiot"]
list_pronouns = ["you", "your", "yours", "you are", "you're", "youre", "u"]
list_requests = ["how", "why", "when", "who", "what", "where", "can", "help", "how?", "why?", "when?", "who?", "what?", "where?", "can?", "help?"]
list_questions = ["?", "??", "???", "??????"]
animation_default = ["bored", "giggling", "confused", "laughing", "afraid", "dog", "heartbroke", "money", "no", "takeoff"]
bot_resp_default = ["I don't think we are getting eachother", "Sounds interesting, maybe you could be more clear?", "Great to have you here. I can do alll sorts of things for you! Ask me for a joke, tell me about yourself "]
list_request_joke = ["tell", "joke", "jokes", "something", "funny"]
jokes_archive = ["Today at the bank, an old lady asked me to help check her balance. So I pushed her over.",
                 "I bought some shoes from a drug dealer. "
                 "I don't know what he laced them with, but I've been tripping all day.",
                 "My boss told me to have a good day.. so I went home.",
                 "The other day, my wife asked me to pass her lipstick but "
                 "I accidentally passed her a glue stick. "
                 "She still isn't talking to me.", "Whatdya call a frenchman wearing sandals? "
                                                   "Phillipe Phillope."]
general_words = ["thanks", "hello", "name"]


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

    if any(word in list_swear for word in user_split_message):
        bot_response = "Please don't swear!"
        animation = "crying"
        return {"animation": animation, "msg": bot_response}

    if any(word in list_pronouns for word in user_split_message):
        bot_response = "This should not be about me, let's talk about you. I am here to help you... How can I help you"
        animation = "excited"
        return {"animation": animation, "msg": bot_response}

    if any(word in list_requests for word in user_split_message):
        question = classify_request(user_message)
        return question

    if any(word in list_request_joke for word in user_split_message):
        animation = animation_default[randomize(5)]
        bot_response = jokes_archive[randomize(5)]
        return {"animation": animation, "msg": bot_response}

    if any(word in general_words for word in user_split_message):
        animation : animation_default[randomize(9)]
        bot_response = bot_resp_default[2]
        return {"animation": animation, "msg": bot_response}

    else:
        return {"animation": animation_default[0], "msg": bot_resp_default[0]}


def randomize(num):
    for x in range(num):
        rand = random.randint(0, num)
        return rand


def classify_request(user_message):
    if any(i in list_questions for i in user_message):
        bot_response = "I'll have to get back to you on that."
        animation = "ok"
        return {"animation": animation, "msg": bot_response}
    else:
        return {"animation": animation_default[1], "msg": bot_resp_default[1]}


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
