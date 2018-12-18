import telepot
import sys
import time
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime
import threading
import copy
from gtts import gTTS
import sqlite3

TOKEN = '750371538:AAHmjwkqqAds28-5T7ssRgmOSzsxia14NXQ'
bot = telepot.Bot(TOKEN)

allreminder = {}
brokenReminder = {}

voice_message = gTTS(text='Hi! this is a reminder', lang='en', slow=False)
voice_message.save("reminder.mp3")

def create_table(table_name, c):
	tn = "U"+str(table_name)
	c.execute('CREATE TABLE IF NOT EXISTS %s (notif TEXT, time TEXT)'%tn)

def insert_in_the_tables(table_name, notif_name, notif_time, db, c):
	tn = "U"+str(table_name)
	c.execute('INSERT INTO %s (notif, time) VALUES(?,?)'%tn, (notif_name, notif_time))
	db.commit()

def delete_notif(c, table_name, notif_name, db):
	tn = "U"+str(table_name)
	c.execute('DELETE FROM %s WHERE notif="%s"'%(tn,notif_name))
	db.commit()

def load_data_from_db():
	my_sqlite = './my_db.sqlite'
	conn = sqlite3.connect(my_sqlite)
	c = conn.cursor()
	c.execute('SELECT name FROM sqlite_master WHERE type="table";'.format(sqlite_master=conn))
	res = c.fetchall()
	for name in res:
		c.execute('SELECT * FROM %s'%name[0])
		all_notifs = c.fetchall()
		for notif in all_notifs:
			if not int(name[0][1:]) in allreminder.keys():
				allreminder[int(name[0][1:])] = {}
			datetime_object = datetime.strptime(notif[1], '%d/%m/%YT%H:%M')
			allreminder[int(name[0][1:])][notif[0]] = [datetime_object, False]


def function_that_reminds():
	threading.Timer(1.0, function_that_reminds).start()
	this_all_reminders = copy.deepcopy(allreminder)
	for chat_id in this_all_reminders.keys():
		for reminder in this_all_reminders[chat_id].keys():
			now = datetime.now()
			now = now.strftime('%d/%m/%YT%H:%M')
			reminder_time = this_all_reminders[chat_id][reminder][0].strftime('%d/%m/%YT%H:%M')
			if reminder_time == now and this_all_reminders[chat_id][reminder][1] == False:
				this_all_reminders[chat_id][reminder][1] = True
				allreminder[chat_id][reminder][1] = True
				bot.sendMessage(chat_id, reminder)
				bot.sendAudio(chat_id, open('reminder.mp3', 'rb'), title='reminder')


def handle(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)

	my_sqlite = './my_db.sqlite'
	conn = sqlite3.connect(my_sqlite)
	c = conn.cursor()
	create_table(chat_id, c)

	if not chat_id in allreminder.keys():
		allreminder[chat_id] = {}

	if content_type == 'text':
		if msg['text'] == '/start':
			bot.sendMessage(chat_id, "please send a message with the format '+ reminder_name 16/11/2018T12:30' to add a reminder and '- reminder_name 16/11/2018T12:30' to delete the reminder")
			bot.sendMessage(chat_id, 'you can also use this custom keyboard',
							reply_markup=ReplyKeyboardMarkup(
								keyboard=[
									[KeyboardButton(text="Done"), KeyboardButton(text="All")]
								]
							))
		elif msg['text'] == 'Done':
			bot.sendMessage(chat_id, 'Reminders added!')
		elif msg['text'] == 'All':
			bot.sendMessage(chat_id, 'All reminders:')
			for x in allreminder[chat_id].keys():
				bot.sendMessage(chat_id, x + ' ' + allreminder[chat_id][x][0].strftime('%d/%m/%YT%H:%M'))
		else:
			splitted_text = msg['text'].split(' ')
			if len(splitted_text) == 3:
				if splitted_text[0] == '+':
					print('adding')
					datetime_object = datetime.strptime(splitted_text[2], '%d/%m/%YT%H:%M')
					allreminder[chat_id][splitted_text[1]] = [datetime_object, False]

					insert_in_the_tables(chat_id, splitted_text[1], splitted_text[2], conn, c)

				elif splitted_text[0] == '-':
					print('deleting')
					datetime_object = datetime.strptime(splitted_text[2], '%d/%m/%YT%H:%M')
					if splitted_text[1] in allreminder[chat_id].keys() and allreminder[chat_id][splitted_text[1]][0] == datetime_object:
						del allreminder[chat_id][splitted_text[1]]
						delete_notif(c, chat_id, splitted_text[1], conn)
			else:
				bot.sendMessage(chat_id, 'invalid format, please use this format: + notif_name date')


def mainFunc():
	MessageLoop(bot, handle).run_as_thread()

	function_that_reminds()
	print('Listening...')

	while 1:
		time.sleep(10)

load_data_from_db()
mainFunc()