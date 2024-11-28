import requests
import schedule
import telebot
import random
import time
import os

from dotenv import load_dotenv

load_dotenv()

TG_TOKEN = os.getenv("TG_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
MESSAGE_THREAD_ID = os.getenv("MESSAGE_THREAD_ID")

bot = telebot.TeleBot(TG_TOKEN)

url = "https://leetcode.com/graphql"

headers = {"Content-Type": "application/json", "Referer": "https://leetcode.com" }

query = """
query getDailyProblem {
    activeDailyCodingChallengeQuestion {
        link
        question {
            title
            difficulty
        }
    }
}
"""

payload = {"query": query}

prephrases = [
    "Код или не код — вот в чём вопрос! 🤔\nСегодняшняя задача: ",
    "Тыж программист? Тогда решай! 🧑‍💻\nВот задача: ",
    "Кто, если не ты? Когда, если не сейчас? 🤓\nТвоя задача: ",
    "Твоя мама не программист, а ты вот должен! 🔥\nДержи задачу: ",
    "Вставай и кодь! 😤\nСегодняшняя задача: ",
    "Сила в тебе велика, джедай кодинга! 🌌\nВот задача: ",
    "Илон Маск уже решил эту задачу! 🚀\nА ты? Вот она: ",
    "Кодить, учиться, побеждать! 🥇\nСегодняшний вызов: ",
    "Проблемы? Нет, только вызовы! 🌟\nЛови задачу: ",
    "Хочешь багов меньше? Решай задач больше! 🐛\nВот тебе задача: ",
    "Бу! Испугался? Не бойся, я друг, я тебя не обижу. Иди сюда, иди ко мне, сядь рядом со мной, посмотри. Ты видишь эту задачу? Я тоже её вижу. Давай смотреть на неё до тех пор, пока мы не решим её. Ты не хочешь? Почему? 👀\nСмотри на задачу: ",
    "Где-то грустный хомяк переживает, что ты ещё не начал тапать! 🐹\nСегодняшняя задача: ",
    "Я не скажу вам:'Let me do it for you!' 🧠\nРешайте эту задачу сами: ",
    "Если решишь эту задачу, то все будут говорить:'Какой же он еб...могучий!' 🐶\nСегодня: ",
    "В 20:31 при... Задачу дня решил и прибыл! 👯\nИ ты реши: ",
    "Стоять, Ковбой! А ты решил задачу? 🤠\nСегодняшняя задача: ",
    "Чтобы кричать 'ГООООЛ' потом, реши задачу сейчас! 🐻\nЗадача: ",
    "Шо ты маленкий, привет, шо ты плачешь или нет? Чтобы не плакать с 0 в кармане: реши задачу сейчас! 😿\nЛови: ",
    "Что за тяги? Такие бархатные тяги, ребята. Фу-уф, кефтеме! Чтобы в будущем щеголять в таких же бархатных, реши задачу и гуляй! 👞\nАУФ: ",
    "Древние Русы сражались против Ящеров, а ты не можешь решить задачу? Слабак! 🦎\nДелай-делай: "
]

def sendDailyProblem(cid, mtid):
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:        
        sonOfJ = response.json()
        question = sonOfJ["data"]["activeDailyCodingChallengeQuestion"]

        link = "https://leetcode.com" + question["link"]
        title = question["question"]["title"]
        difficulty = question["question"]["difficulty"]

        rnum = random.randint(0, 19)

        message = prephrases[rnum] + title + "\n" + "Difficulty: " + difficulty + "\n" + link
        
        bot.send_message(chat_id=cid, message_thread_id=mtid, text=message)
    else:
        message = "Error: response HTTP status is different from 200"
        bot.send_message(chat_id=cid, message_thread_id=mtid, text=message)

def sendWrapper():
    sendDailyProblem(CHAT_ID, MESSAGE_THREAD_ID)

schedule.every().day.at("04:00").do(sendWrapper)
schedule.every().day.at("16:00").do(sendWrapper)

while True:
    schedule.run_pending()
    time.sleep(1)
