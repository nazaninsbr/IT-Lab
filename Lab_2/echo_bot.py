import telepot
import sys
import time
from telepot.loop import MessageLoop

TOKEN = '750371538:AAHmjwkqqAds28-5T7ssRgmOSzsxia14NXQ'
bot = telepot.Bot(TOKEN)

def handle(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	print(content_type, chat_type, chat_id)

	if content_type=='text':
		bot.sendMessage(chat_id, msg['text'])

def mainFunc():
	MessageLoop(bot, handle).run_as_thread()
	print('Listening...')

	while 1:
		time.sleep(10)

mainFunc()