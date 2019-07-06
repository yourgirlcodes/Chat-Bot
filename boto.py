"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request, response
import json
import random


list_swear = ["fuck", "shit", "motherfucker", "bitch", "slut", "whore", "idiot"]
list_pronouns = ["you", "your", "yours", "you are", "you're", "youre", "u"]
list_requests = ["how", "why", "when", "who", "what", "where", "can", "help", "how?", "why?", "when?", "who?", "what?",
                 "where?", "can?", "help?"]
list_questions = ["?", "??", "???", "??????"]
animation_default = ["bored", "giggling", "confused", "laughing", "afraid", "dog", "heartbroke", "money", "no", "takeoff"]
bot_resp_default = ["I don't think we are getting eachother", "Sounds interesting, maybe you could be more clear?",
                    "Great to have you here. I can do alll sorts of things for you! "
                    "Ask me for a joke, tell me about yourself "]
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
dog_fact = ["Dogs and cats both slurp water the same way.",
            "Your dog’s sense of smell is 1,000 to 10 million times better than yours.",
            "Dogs can hear 4 times as far as humans.",
            "Your dog can smell your feelings."]
dog_words = ["dogs", "dogs?", "doggy", "puppy", "dog?", "dog"]


@route('/', method='GET')
def index():
    return template("chatbot.html")


@route('/hello')
def hello_again():
    if request.get_cookie("visited"):
        return "Hey, you're back!"
    else:
        response.set_cookie("visited", "yes")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg').lower()
    if request.get_cookie("visited"):
        feedback = conversation(user_message)
        return feedback
    else:
        response.set_cookie("visited", "yes")
        feedback = handle_first_question(user_message)
        return feedback


def conversation(user_message):
    bot_output = parsing(user_message)
    return json.dumps(bot_output)


def handle_first_question(user_message):
    bot_response = ("Hey %s!" % user_message)
    return json.dumps({"animation": "giggling", "msg": bot_response})


def parsing(user_message):
    user_split_message = user_message.split(" ")

    if any(word in list_swear for word in user_split_message):
        bot_response = "Please don't swear!"
        animation = "crying"
        return {"animation": animation, "msg": bot_response}

    if any(word in list_pronouns for word in user_split_message):
        bot_response = "You seem to really like me."
        animation = "excited"
        return {"animation": animation, "msg": bot_response}

    if '?' in user_message:
        question = classify_request(user_split_message)
        return question

    if any(word in list_request_joke for word in user_split_message):
        animation = animation_default[randomize(5)]
        bot_response = jokes_archive[randomize(4)]
        return {"animation": animation, "msg": bot_response}

    if any(word in general_words for word in user_split_message):
        animation = animation_default[randomize(8)]
        bot_response = bot_resp_default[2]
        return {"animation": animation, "msg": bot_response}

    else:
        return {"animation": animation_default[0], "msg": bot_resp_default[0]}


def randomize(num):
    for x in range(num):
        rand = random.randint(0, num)
        return rand


def classify_request(user_split_message):
    if any(word in dog_words for word in user_split_message):
        return {"animation": "dog", "msg": dog_fact[randomize(3)]}
    else:
        bot_response = 'If you are trying to ask me a question, ' \
                       'I only know how to tell you about dogs. so type \'dogs\' ' \
                       'along with what you would like to know... ' \
                       'eg: \'dogs ? -  and I will tell you a random dog fact.'
        animation = "dog"
        return {"animation": animation, "msg": bot_response}


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
