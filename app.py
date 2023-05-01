import telebot, random
from telebot import custom_filters
import config										#config.py здесь хранятся все глобальные переменные

if config.TOKEN == "put your token here": 
	print("put your token in config.py file")
	exit()
if config.ADMIN == "put your own username here":
	print("put admin username in config.py file")
	exit()
bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['enable'])			#флаг для временного отключения бота, работает на глобальных переменных указанных в config.py, 
def enable(message):								#да глобальные перемнные это плохо, но мне так проще да и ***** впринципе
	if message.from_user.username != config.ADMIN[1:]:
		bot.reply_to(message, f"У пользователя @{message.from_user.username} недостаточно прав для доступа к этой функции")
		return
	config.FLAG = True
	bot.reply_to(message, "done")	

@bot.message_handler(commands=['disable'])
def disable(message):
	if message.from_user.username != config.ADMIN[1:]:
		bot.reply_to(message, f"У пользователя @{message.from_user.username} недостаточно прав для доступа к этой функции")
		return
	config.FLAG = False
	bot.reply_to(message, "done")

@bot.message_handler(commands=['enable_bulling'])	#флаг для перехода в режим булинга, работает на глобальных переменных указанных в config.py, 
def enable_bulling(message):						#да глобальные перемнные это плохо, но мне так проще да и ***** впринципе
	if len(message.text.split()) > 1:
		config.DODIK = message.text.split()[1]
		if config.DODIK == config.ADMIN:
			bot.reply_to(message, f"Невозможно активировать для этого пользователя")
			return
		if config.DODIK[0] == "@":
			config.DODIK = config.DODIK[1:]
			config.INITIATOR = message.from_user.username
			bot.reply_to(message, "done")
			return
	bot.reply_to(message, """syntax error
/enable_bulling @*username*""")

@bot.message_handler(commands=['disable_bulling'])
def disable_bulling(message):	
	if (message.from_user.username == config.ADMIN[1:]) or (message.from_user.username == config.INITIATOR):
		config.DODIK = ""
		config.INITIATOR = ""
		bot.reply_to(message, "done")
		return
	bot.reply_to(message, f"У пользователя @{message.from_user.username} недостаточно прав для доступа к этой функции")	

@bot.message_handler(commands=['status'])
def status(message):
	bot.reply_to(message, f"""enabled = {config.FLAG}
bulling_enabled = {bool(config.DODIK)}""")

@bot.message_handler(content_types=config.TYPES)
def reply_to_any(message):
	if message.from_user.username == config.DODIK: #клоунада
		bot.reply_to(message, "🤡")	
	elif config.FLAG:
		bot.reply_to(message, random.choice(config.SMILES))
print("started")
bot.add_custom_filter(custom_filters.ChatFilter())
bot.infinity_polling()