import requests
import schedule
import telebot
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

def sendDailyProblem(cid, mtid):
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:        
        sonOfJ = response.json()
        question = sonOfJ["data"]["activeDailyCodingChallengeQuestion"]

        link = "https://leetcode.com" + question["link"]
        title = question["question"]["title"]
        difficulty = question["question"]["difficulty"]

        message = title + "\n" + "Difficulty: " + difficulty + "\n" + link
        
    bot.send_message(chat_id=cid, message_thread_id=mtid, text=message)

def sendWrapper():
    sendDailyProblem(CHAT_ID, MESSAGE_THREAD_ID)

schedule.every().day.at("04:00").do(sendWrapper)
schedule.every().day.at("16:00").do(sendWrapper)

while True:
    schedule.run_pending()
    time.sleep(1)
