import configparser
import json

from telethon.sync import TelegramClient
from telethon import connection


from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.messages import GetHistoryRequest


# for changing time in JSON file
from datetime import date, datetime


# Считываем учетные данные
config = configparser.ConfigParser()
config.read("config.ini")

# Присваиваем значения внутренним переменным
api_id   = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']


client = TelegramClient(username, api_id, api_hash)

client.start()


async def find_participants(channel):
	startUser = 0
	limitUsers = 100

	allParticipants = []
	filter = ChannelParticipantsSearch('')

	while True:
		participants = await client(GetParticipantsRequest(channel,
			filter, startUser, limitUsers, hash=0))
		if not participants.users:
			break
		allParticipants.extend(participants.users)
		startUser += len(participants.users)

	usersInformation = []

	for participant in allParticipants:
		usersInformation.append({"id": participant.id,
			"first_name": participant.first_name,
			"last_name": participant.last_name,
			"user": participant.username,
			"phone": participant.phone,
			"is_bot": participant.bot})

	with open('channel_users.json', 'w', encoding='utf8') as outfile:
		json.dump(usersInformation, outfile, ensure_ascii=False)


async def find_messages(channel):
	startMsg = 0
	limitMsg = 50

	allMessages = []
	totalMessages = 0
	noMoreMessages = 1000

	class DateTimeEncoder(json.JSONEncoder):
		def default(self, o):
			if isinstance(o, datetime):
				return o.isoformat()
			if isinstance(o, bytes):
				return list(o)
			return json.JSONEncoder.default(self, o)

	while True:
		history = await client(GetHistoryRequest(
			peer=channel,
			offset_id=startMsg,
			offset_date=None, add_offset=0,
			limit=limitMsg, max_id=0, min_id=0,
			hash=0))
		if not history.messages:
			break
		messages = history.messages
		for message in messages:
			allMessages.append(message.to_dict())
			print(message.to_dict())
		startMsg = messages[len(messages) - 1].id
		totalMessages = len(allMessages)
		if noMoreMessages != 0 and totalMessages >= noMoreMessages:
			break

	with open('channel_messages.json', 'w', encoding='utf8') as outfile:
		 json.dump(allMessages, outfile, ensure_ascii=False, cls=DateTimeEncoder)


async def main():
	url = input("Введите ссылку на канал или чат: ")
	channel = await client.get_entity(url)
	#await find_participants(channel)
	await find_messages(channel)


with client:
	client.loop.run_until_complete(main())