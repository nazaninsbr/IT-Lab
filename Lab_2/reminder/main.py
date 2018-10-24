import telepot
import sys
import time
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime
import threading
import copy 

TOKEN = '750371538:AAHmjwkqqAds28-5T7ssRgmOSzsxia14NXQ'
bot = telepot.Bot(TOKEN)

allreminder = {}

def function_that_reminds():
	threading.Timer(1.0, function_that_reminds).start()
	this_all_reminders = copy.deepcopy(allreminder)
	for chat_id in this_all_reminders.keys():
		for reminder in this_all_reminders[chat_id].keys():
			now = datetime.now()
			now = now.strftime('%d/%m/%YT%H:%M')
			reminder_time = this_all_reminders[chat_id][reminder][0].strftime('%d/%m/%YT%H:%M')
			if reminder_time == now and this_all_reminders[chat_id][reminder][1]==False:
				bot.sendMessage(chat_id, reminder)
				this_all_reminders[chat_id][reminder][1]=True
				allreminder[chat_id][reminder][1]=True

def handle(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	
	bot.sendMessage(chat_id, 'testing custom keyboard',
							reply_markup=ReplyKeyboardMarkup(
								keyboard=[
									[KeyboardButton(text="Add"), KeyboardButton(text="Remove")]
								]
							))

	if not chat_id in allreminder.keys():
		allreminder[chat_id] = {}

	if content_type=='text':
		if msg['text'] == '/Done':
			bot.sendMessage(chat_id, 'you have the following reminders:')
			for x in allreminder[chat_id].keys():
				bot.sendMessage(chat_id, x+' '+allreminder[chat_id][x][0].strftime('%d/%m/%YT%H:%M'))
		else:
			splitted_text  = msg['text'].split(' ')
			if len(splitted_text)==3:
				if splitted_text[0]=='+':
					print('adding')
					datetime_object = datetime.strptime(splitted_text[2], '%d/%m/%YT%H:%M')
					allreminder[chat_id][splitted_text[1]] = [datetime_object , False]
				elif splitted_text[0]=='-':
					print('deleting')
					datetime_object = datetime.strptime(splitted_text[2], '%d/%m/%YT%H:%M')
					if splitted_text[1] in allreminder[chat_id].keys() and allreminder[chat_id][splitted_text[1]][0] == datetime_object:
						del allreminder[chat_id][splitted_text[1]]
			else:
				bot.sendMessage(chat_id, 'invalid format, please use this format: + notif_name date')

def mainFunc():
	MessageLoop(bot, handle).run_as_thread()
	function_that_reminds()
	print('Listening...')

	while 1:
		time.sleep(10)

mainFunc()